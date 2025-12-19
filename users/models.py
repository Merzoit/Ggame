from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class TelegramUser(AbstractUser):
    """
    Пользователь Telegram с расширенными полями для игры
    """
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='telegram_users'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='telegram_users'
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Telegram ID"),
        help_text=_("Уникальный идентификатор пользователя в Telegram")
    )
    username_telegram = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Telegram Username"),
        help_text=_("Имя пользователя в Telegram")
    )
    first_name_telegram = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Имя в Telegram")
    )
    last_name_telegram = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Фамилия в Telegram")
    )

    # Статистика игрока
    total_games = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Всего игр")
    )
    games_won = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Побед")
    )
    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Общий счет")
    )
    current_streak = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Текущая серия побед")
    )
    best_streak = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Лучшая серия побед")
    )

    # Настройки
    notifications_enabled = models.BooleanField(
        default=True,
        verbose_name=_("Уведомления включены")
    )
    language = models.CharField(
        max_length=10,
        default='ru',
        choices=[
            ('ru', _('Русский')),
            ('en', _('English')),
        ],
        verbose_name=_("Язык")
    )

    # Даты
    date_joined_telegram = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата регистрации в Telegram")
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Последняя активность")
    )

    class Meta:
        verbose_name = _("Пользователь Telegram")
        verbose_name_plural = _("Пользователи Telegram")
        ordering = ['-total_points', '-date_joined_telegram']

    def __str__(self):
        return f"{self.username_telegram or self.telegram_id} ({self.total_points} pts)"

    def get_win_rate(self):
        """Возвращает процент побед"""
        if self.total_games == 0:
            return 0
        return round((self.games_won / self.total_games) * 100, 1)

    def update_stats(self, won=False, points=0):
        """Обновляет статистику после игры"""
        self.total_games += 1
        self.total_points += points

        if won:
            self.games_won += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        else:
            self.current_streak = 0

        self.save(update_fields=[
            'total_games', 'games_won', 'total_points',
            'current_streak', 'best_streak'
        ])
