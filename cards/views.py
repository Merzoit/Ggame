from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import AnimeUniverse, Season, CardTemplate, CardInstance, Deck, DeckCard
from .serializers import (
    AnimeUniverseSerializer, SeasonSerializer,
    CardTemplateSerializer, CardInstanceSerializer,
    DeckSerializer, DeckCardSerializer
)


class AnimeUniverseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра аниме-вселенных
    """
    queryset = AnimeUniverse.objects.filter(is_active=True)
    serializer_class = AnimeUniverseSerializer
    permission_classes = [IsAuthenticated]


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра сезонов
    """
    queryset = Season.objects.filter(is_active=True)
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтр по аниме-вселенной"""
        queryset = Season.objects.filter(is_active=True)
        universe_id = self.request.query_params.get('universe', None)
        if universe_id:
            queryset = queryset.filter(anime_universe_id=universe_id)
        return queryset


class CardTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра шаблонов карт
    """
    queryset = CardTemplate.objects.filter(is_active=True)
    serializer_class = CardTemplateSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def instances(self, request, pk=None):
        """Получить все экземпляры этой карты у игрока"""
        template = self.get_object()
        instances = CardInstance.objects.filter(
            template=template,
            owner=request.user
        )
        serializer = CardInstanceSerializer(instances, many=True)
        return Response(serializer.data)


class CardInstanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления картами игрока
    """
    serializer_class = CardInstanceSerializer

    def get_permissions(self):
        """Разрешить доступ без аутентификации для запросов с telegram_id"""
        if self.request.query_params.get('telegram_id') or self.action == 'get_user_profile':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Возвращает карты пользователя (по telegram_id или текущего)"""
        telegram_id = self.request.query_params.get('telegram_id')
        if telegram_id:
            # Получаем пользователя по telegram_id
            try:
                from users.models import TelegramUser
                user = TelegramUser.objects.get(telegram_id=telegram_id)
                return CardInstance.objects.filter(owner=user)
            except TelegramUser.DoesNotExist:
                return CardInstance.objects.none()

        # Для аутентифицированных пользователей - их карты
        if self.request.user.is_authenticated:
            return CardInstance.objects.filter(owner=self.request.user)

        return CardInstance.objects.none()

    @action(detail=False, methods=['post'])
    def acquire_card(self, request):
        """Получить новую карту (из шаблона)"""
        template_id = request.data.get('template_id')
        if not template_id:
            return Response(
                {'error': 'Не указан template_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            template = CardTemplate.objects.get(id=template_id, is_active=True)
        except CardTemplate.DoesNotExist:
            return Response(
                {'error': 'Шаблон карты не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем стоимость
        user = request.user
        if user.coins < template.coin_cost or user.gold < template.gold_cost:
            return Response(
                {'error': 'Недостаточно валюты'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Списываем стоимость
        user.coins -= template.coin_cost
        user.gold -= template.gold_cost
        user.save()

        # Создаем карту (характеристики сгенерируются автоматически)
        card_instance = CardInstance.objects.create(
            template=template,
            owner=user
        )

        serializer = self.get_serializer(card_instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_deck(self, request, pk=None):
        """Добавить/убрать карту из колоды"""
        card = self.get_object()
        card.is_in_deck = not card.is_in_deck
        card.save()

        serializer = self.get_serializer(card)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reset_health(self, request, pk=None):
        """Восстановить здоровье карты"""
        card = self.get_object()
        card.reset_health()

        serializer = self.get_serializer(card)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def sell_card(self, request, pk=None):
        """Продать карту"""
        card = self.get_object()
        sell_price = card.template.sell_price

        # Начисляем монеты игроку
        card.owner.coins += sell_price
        card.owner.save()

        # Удаляем карту
        card.delete()

        return Response({
            'message': f'Карта продана за {sell_price} монет',
            'coins_earned': sell_price
        })

    @action(detail=False, methods=['get'])
    def get_user_profile(self, request):
        """Получить профиль пользователя с его картами и колодой"""
        telegram_id = request.query_params.get('telegram_id')

        if telegram_id:
            # Получаем пользователя по telegram_id
            try:
                from users.models import TelegramUser
                user = TelegramUser.objects.get(telegram_id=telegram_id)
            except TelegramUser.DoesNotExist:
                return Response(
                    {'error': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif request.user.is_authenticated:
            user = request.user
        else:
            return Response(
                {'error': 'Необходима аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Получаем карты пользователя
        cards = CardInstance.objects.filter(owner=user)

        # Получить или создать колоду
        deck, created = Deck.objects.get_or_create(owner=user)

        # Получаем карты колоды с деталями
        deck_cards_data = []
        for deck_card in deck.deck_cards.select_related('card__template').all():
            card = deck_card.card
            deck_cards_data.append({
                'id': card.id,
                'position': deck_card.position,
                'template': {
                    'id': card.template.id,
                    'name': card.template.name,
                    'element': card.template.element,
                },
                'health': card.health,
                'attack': card.attack,
                'defense': card.defense,
            })

        return Response({
            'user': {
                'id': user.id,
                'telegram_id': user.telegram_id,
                'username': user.username,
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'total_games': user.total_games,
                'games_won': user.games_won,
                'total_points': user.total_points,
                'current_streak': user.current_streak,
                'best_streak': user.best_streak,
                'coins': user.coins,
                'gems': user.gems,
                'win_rate': user.win_rate,
            },
            'cards': [{
                'id': card.id,
                'template': {
                    'id': card.template.id,
                    'name': card.template.name,
                    'element': card.template.element,
                },
                'health': card.health,
                'attack': card.attack,
                'defense': card.defense,
                'acquired_at': card.acquired_at.isoformat(),
            } for card in cards],
            'deck': {
                'id': deck.id,
                'name': deck.name,
                'cards': deck_cards_data,
            },
        })


class DeckViewSet(viewsets.ViewSet):
    """
    ViewSet для управления колодой игрока (одна на игрока)
    """
    permission_classes = [IsAuthenticated]

    def get_deck(self):
        """Получить или создать колоду для пользователя"""
        deck, created = Deck.objects.get_or_create(
            owner=self.request.user,
            defaults={'name': 'Моя колода'}
        )
        return deck

    def retrieve(self, request):
        """Получить колоду пользователя"""
        deck = self.get_deck()
        serializer = DeckSerializer(deck)
        return Response(serializer.data)

    def update(self, request):
        """Обновить колоду пользователя"""
        deck = self.get_deck()
        serializer = DeckSerializer(deck, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def add_card(self, request):
        """Добавить карту в колоду"""
        deck = self.get_deck()
        card_id = request.data.get('card_id')
        position = request.data.get('position')

        if not card_id or not position:
            return Response(
                {'error': 'Не указаны card_id и position'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            card = CardInstance.objects.get(id=card_id, owner=request.user)
        except CardInstance.DoesNotExist:
            return Response(
                {'error': 'Карта не найдена в вашем инвентаре'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем позицию
        if position < 1 or position > 3:
            return Response(
                {'error': 'Позиция должна быть от 1 до 3'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем уникальность шаблонов в колоде
        existing_templates = set()
        for deck_card in deck.deck_cards.all():
            existing_templates.add(deck_card.card.template_id)

        if card.template_id in existing_templates:
            return Response(
                {'error': 'Карта с таким шаблоном уже есть в колоде'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем или обновляем связь
        deck_card, created = DeckCard.objects.get_or_create(
            deck=deck,
            position=position,
            defaults={'card': card}
        )

        if not created:
            # Если позиция занята, заменяем карту
            deck_card.card = card
            deck_card.save()

        serializer = DeckSerializer(deck)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_card(self, request):
        """Убрать карту из колоды"""
        deck = self.get_deck()
        position = request.data.get('position')

        if not position:
            return Response(
                {'error': 'Не указана позиция'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            deck_card = DeckCard.objects.get(deck=deck, position=position)
            deck_card.delete()

            serializer = DeckSerializer(deck)
            return Response(serializer.data)

        except DeckCard.DoesNotExist:
            return Response(
                {'error': 'Карта в указанной позиции не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def deck(self, request):
        """Получить карты в колоде"""
        deck_cards = self.get_queryset().filter(is_in_deck=True)
        serializer = self.get_serializer(deck_cards, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def collection(self, request):
        """Получить сводку коллекции карт"""
        instances = self.get_queryset()

        # Группируем по шаблонам
        templates_count = {}
        for instance in instances:
            template_name = instance.template.name
            templates_count[template_name] = templates_count.get(template_name, 0) + 1

        # Статистика по редкости
        rarity_stats = {}
        for instance in instances:
            rarity = instance.template.get_rarity_display()
            rarity_stats[rarity] = rarity_stats.get(rarity, 0) + 1

        return Response({
            'total_cards': instances.count(),
            'unique_templates': len(templates_count),
            'templates_breakdown': templates_count,
            'rarity_breakdown': rarity_stats,
            'deck_size': instances.filter(is_in_deck=True).count(),
        })
