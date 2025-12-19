from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CardTemplate, CardInstance
from .serializers import CardTemplateSerializer, CardInstanceSerializer


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
