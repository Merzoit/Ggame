from django.contrib import admin
from .models import Item, InventoryItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Админка для предметов
    """
    list_display = [
        'name', 'rarity', 'item_type', 'coin_cost', 'gold_cost',
        'max_stack', 'is_stackable', 'is_active'
    ]
    list_filter = ['rarity', 'item_type', 'is_stackable', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['coin_cost', 'gold_cost', 'is_active']

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Свойства', {
            'fields': ('rarity', 'item_type', 'max_stack', 'is_stackable')
        }),
        ('Стоимость', {
            'fields': ('coin_cost', 'gold_cost')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """
    Админка для предметов в инвентаре
    """
    list_display = [
        'player', 'item', 'quantity', 'acquired_at'
    ]
    list_filter = ['item__rarity', 'item__item_type', 'acquired_at']
    search_fields = [
        'player__username_telegram',
        'player__first_name_telegram',
        'item__name'
    ]
    raw_id_fields = ['player', 'item']  # Для больших списков

    fieldsets = (
        (None, {
            'fields': ('player', 'item', 'quantity')
        }),
        ('Информация', {
            'fields': ('acquired_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['acquired_at']
