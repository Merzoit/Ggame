from django.contrib import admin
from .models import CardTemplate, CardInstance


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    """
    Админка для шаблонов карт
    """
    list_display = [
        'name', 'rarity', 'element', 'anime_universe', 'season',
        'health_min', 'health_max', 'attack_min', 'attack_max',
        'coin_cost', 'gold_cost', 'is_active'
    ]
    list_filter = [
        'rarity', 'element', 'anime_universe', 'season', 'is_active'
    ]
    search_fields = ['name', 'anime_universe', 'season', 'description']
    list_editable = ['coin_cost', 'gold_cost', 'is_active']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image_url')
        }),
        ('Принадлежность', {
            'fields': ('anime_universe', 'season')
        }),
        ('Характеристики', {
            'fields': ('rarity', 'element')
        }),
        ('Диапазоны характеристик', {
            'fields': (
                ('health_min', 'health_max'),
                ('attack_min', 'attack_max'),
                ('defense_min', 'defense_max')
            )
        }),
        ('Стоимость', {
            'fields': (('coin_cost', 'gold_cost'),)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )

    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related()


@admin.register(CardInstance)
class CardInstanceAdmin(admin.ModelAdmin):
    """
    Админка для карт игроков
    """
    list_display = [
        'template', 'owner', 'health', 'attack', 'defense',
        'current_health', 'level', 'is_in_deck', 'acquired_at'
    ]
    list_filter = [
        'template__rarity', 'template__element', 'template__anime_universe',
        'is_in_deck', 'level', 'acquired_at'
    ]
    search_fields = [
        'template__name', 'owner__username_telegram',
        'owner__first_name_telegram'
    ]
    raw_id_fields = ['template', 'owner']  # Для больших списков

    fieldsets = (
        (None, {
            'fields': ('template', 'owner')
        }),
        ('Характеристики', {
            'fields': ('health', 'attack', 'defense', 'current_health')
        }),
        ('Прогресс', {
            'fields': ('level', 'experience', 'is_in_deck')
        }),
        ('Время', {
            'fields': ('acquired_at', 'last_used'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['acquired_at', 'last_used']

    actions = ['reset_health', 'regenerate_stats']

    def reset_health(self, request, queryset):
        """Восстановить здоровье выбранных карт"""
        updated = queryset.update(current_health=models.F('health'))
        self.message_user(
            request,
            f'Здоровье восстановлено для {updated} карт.'
        )
    reset_health.short_description = "Восстановить здоровье"

    def regenerate_stats(self, request, queryset):
        """Перегенерировать характеристики карт"""
        for card in queryset:
            card.regenerate_stats()
        self.message_user(
            request,
            f'Характеристики перегенерированы для {queryset.count()} карт.'
        )
    regenerate_stats.short_description = "Перегенерировать характеристики"
