from rest_framework import serializers
from .models import Item, InventoryItem


class ItemSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов"""

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'rarity', 'item_type',
            'coin_cost', 'gold_cost', 'max_stack', 'is_stackable'
        ]


class InventoryItemSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов в инвентаре"""
    item = ItemSerializer(read_only=True)
    player_username = serializers.CharField(
        source='player.username_telegram',
        read_only=True
    )

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'player', 'player_username', 'item',
            'quantity', 'acquired_at'
        ]
        read_only_fields = ['id', 'player', 'acquired_at']
