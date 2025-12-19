from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(UserAdmin):
    """
    Админка для пользователей Telegram
    """
    # Поля для отображения в списке
    list_display = [
        'telegram_id', 'username_telegram', 'first_name_telegram',
        'last_name_telegram', 'total_games', 'games_won', 'total_points',
        'coins', 'gold', 'is_active', 'date_joined_telegram'
    ]

    # Поля для фильтрации
    list_filter = [
        'is_active', 'is_staff', 'is_superuser',
        'language', 'notifications_enabled', 'date_joined_telegram'
    ]

    # Поля для поиска
    search_fields = [
        'telegram_id', 'username', 'username_telegram',
        'first_name_telegram', 'last_name_telegram', 'email'
    ]

    # Группировка полей в форме
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram информация', {
            'fields': (
                'telegram_id', 'username_telegram',
                'first_name_telegram', 'last_name_telegram',
                'date_joined_telegram', 'last_activity'
            ),
        }),
        ('Игровая статистика', {
            'fields': (
                'total_games', 'games_won', 'total_points',
                'current_streak', 'best_streak'
            ),
        }),
        ('Валюта', {
            'fields': ('coins', 'gold'),
        }),
        ('Настройки', {
            'fields': ('notifications_enabled', 'language'),
        }),
    )

    # Поля только для чтения
    readonly_fields = ['date_joined_telegram', 'last_activity']

    # Сортировка по умолчанию
    ordering = ['-total_points', '-date_joined_telegram']

    # Количество элементов на странице
    list_per_page = 50
