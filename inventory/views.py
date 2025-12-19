from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item, InventoryItem
from .serializers import ItemSerializer, InventoryItemSerializer


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра предметов
    """
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления инвентарем игрока
    """
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает только предметы текущего пользователя"""
        return InventoryItem.objects.filter(player=self.request.user)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Добавить предмет в инвентарь"""
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)

        try:
            item = Item.objects.get(id=item_id, is_active=True)
        except Item.DoesNotExist:
            return Response(
                {'error': 'Предмет не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, есть ли уже такой предмет у игрока
        inventory_item, created = InventoryItem.objects.get_or_create(
            player=request.user,
            item=item,
            defaults={'quantity': 0}
        )

        if inventory_item.add_quantity(quantity):
            serializer = self.get_serializer(inventory_item)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Невозможно добавить предмет (превышен лимит стопки)'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Убрать предмет из инвентаря"""
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)

        try:
            inventory_item = InventoryItem.objects.get(
                player=request.user,
                item_id=item_id
            )
        except InventoryItem.DoesNotExist:
            return Response(
                {'error': 'Предмет не найден в инвентаре'},
                status=status.HTTP_404_NOT_FOUND
            )

        if inventory_item.remove_quantity(quantity):
            return Response({'success': True})
        else:
            return Response(
                {'error': 'Недостаточно предметов'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Получить сводку инвентаря"""
        inventory_items = self.get_queryset()
        total_items = sum(item.quantity for item in inventory_items)

        items_by_type = {}
        items_by_rarity = {}

        for item in inventory_items:
            item_type = item.item.get_item_type_display()
            rarity = item.item.get_rarity_display()

            items_by_type[item_type] = items_by_type.get(item_type, 0) + item.quantity
            items_by_rarity[rarity] = items_by_rarity.get(rarity, 0) + item.quantity

        return Response({
            'total_items': total_items,
            'total_unique_items': inventory_items.count(),
            'items_by_type': items_by_type,
            'items_by_rarity': items_by_rarity,
        })
