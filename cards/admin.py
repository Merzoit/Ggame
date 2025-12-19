from django.contrib import admin
from .models import AnimeUniverse, Season, CardTemplate, CardInstance


@admin.register(AnimeUniverse)
class AnimeUniverseAdmin(admin.ModelAdmin):
    """
    Админка для аниме-вселенных
    """
    list_display = ['name', 'is_active', 'season_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

    def season_count(self, obj):
        return obj.seasons.count()
    season_count.short_description = "Количество сезонов"


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """
    Админка для сезонов
    """
    list_display = ['name', 'anime_universe', 'season_number', 'is_active']
    list_filter = ['anime_universe', 'is_active']
    search_fields = ['name', 'anime_universe__name']
    list_editable = ['is_active']


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    """
    Админка для шаблонов карт
    """
    list_display = [
        'name', 'element', 'anime_universe', 'season',
        'health_min', 'health_max', 'attack_min', 'attack_max',
        'coin_cost', 'gold_cost', 'sell_price', 'is_active'
    ]
    list_filter = [
        'element', 'anime_universe', 'season', 'is_active'
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
            'fields': ('element',)
        }),
        ('Диапазоны характеристик', {
            'fields': (
                ('health_min', 'health_max'),
                ('attack_min', 'attack_max'),
                ('defense_min', 'defense_max')
            )
        }),
        ('Стоимость', {
            'fields': (('coin_cost', 'gold_cost'), ('sell_price',))
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
        'template__element', 'template__anime_universe',
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
