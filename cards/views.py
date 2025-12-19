from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает только карты текущего пользователя"""
        return CardInstance.objects.filter(owner=self.request.user)

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


class DeckViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления колодами игрока
    """
    serializer_class = DeckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает только колоды текущего пользователя"""
        return Deck.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Создание колоды для текущего пользователя"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_card(self, request, pk=None):
        """Добавить карту в колоду"""
        deck = self.get_object()
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

        # Проверяем, что карта не используется в другой колоде
        if DeckCard.objects.filter(card=card).exclude(deck=deck).exists():
            return Response(
                {'error': 'Эта карта уже используется в другой колоде'},
                status=status.HTTP_400_BAD_REQUEST
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

        serializer = self.get_serializer(deck)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_card(self, request, pk=None):
        """Убрать карту из колоды"""
        deck = self.get_object()
        position = request.data.get('position')

        if not position:
            return Response(
                {'error': 'Не указана позиция'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            deck_card = DeckCard.objects.get(deck=deck, position=position)
            deck_card.delete()

            serializer = self.get_serializer(deck)
            return Response(serializer.data)

        except DeckCard.DoesNotExist:
            return Response(
                {'error': 'Карта в указанной позиции не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        """Сделать колоду активной"""
        deck = self.get_object()

        # Проверяем валидность колоды
        is_valid, message = deck.is_valid()
        if not is_valid:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Деактивируем все другие колоды пользователя
        Deck.objects.filter(owner=request.user).update(is_active=False)

        # Активируем эту колоду
        deck.is_active = True
        deck.save()

        serializer = self.get_serializer(deck)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active_deck(self, request):
        """Получить активную колоду"""
        try:
            deck = Deck.objects.get(owner=request.user, is_active=True)
            serializer = self.get_serializer(deck)
            return Response(serializer.data)
        except Deck.DoesNotExist:
            return Response(
                {'error': 'Активная колода не найдена'},
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
