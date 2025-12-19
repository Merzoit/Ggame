from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import TelegramUser


class GameSession(models.Model):
    """
    Игровая сессия
    """
    STATUS_CHOICES = [
        ('waiting', _('Ожидание игроков')),
        ('active', _('Активная')),
        ('finished', _('Завершена')),
        ('cancelled', _('Отменена')),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting',
        verbose_name=_("Статус")
    )
    players = models.ManyToManyField(
        TelegramUser,
        through='PlayerInGame',
        verbose_name=_("Игроки")
    )
    max_players = models.PositiveIntegerField(
        default=4,
        verbose_name=_("Максимум игроков")
    )

    # Настройки игры
    time_limit = models.PositiveIntegerField(
        default=30,
        verbose_name=_("Время на игру (минуты)")
    )
    points_for_win = models.PositiveIntegerField(
        default=100,
        verbose_name=_("Очки за победу")
    )

    # Telegram чат
    telegram_chat_id = models.BigIntegerField(
        verbose_name=_("Telegram Chat ID")
    )
    telegram_message_id = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Telegram Message ID")
    )

    # Время
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Создана")
    )
    started_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Начата")
    )
    finished_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Завершена")
    )

    class Meta:
        verbose_name = _("Игровая сессия")
        verbose_name_plural = _("Игровые сессии")
        ordering = ['-created_at']

    def __str__(self):
        return f"Game {self.id} - {self.get_status_display()} ({self.players.count()}/{self.max_players})"

    def start_game(self):
        """Начинает игру"""
        if self.status == 'waiting' and self.players.count() >= 2:
            self.status = 'active'
            self.started_at = timezone.now()
            self.save()
            return True
        return False

    def finish_game(self, winner=None):
        """Завершает игру"""
        self.status = 'finished'
        self.finished_at = timezone.now()
        self.save()

        # Обновляем статистику игроков
        for player_in_game in self.player_in_game.all():
            won = player_in_game.player == winner if winner else False
            player_in_game.player.update_stats(won=won, points=player_in_game.points)


class PlayerInGame(models.Model):
    """
    Игрок в конкретной игре
    """
    player = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name=_("Игрок")
    )
    game_session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE,
        related_name='player_in_game',
        verbose_name=_("Игровая сессия")
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Присоединился")
    )
    points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Очки в игре")
    )
    is_ready = models.BooleanField(
        default=False,
        verbose_name=_("Готов к игре")
    )

    class Meta:
        verbose_name = _("Игрок в игре")
        verbose_name_plural = _("Игроки в играх")
        unique_together = ['player', 'game_session']

    def __str__(self):
        return f"{self.player} in {self.game_session}"


class Question(models.Model):
    """
    Вопрос для игры
    """
    DIFFICULTY_CHOICES = [
        ('easy', _('Легкий')),
        ('medium', _('Средний')),
        ('hard', _('Сложный')),
    ]

    text = models.TextField(
        verbose_name=_("Текст вопроса")
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name=_("Сложность")
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Категория")
    )
    correct_answer = models.TextField(
        verbose_name=_("Правильный ответ")
    )

    # Статистика
    times_asked = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Количество показов")
    )
    correct_answers = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Правильных ответов")
    )

    # Мета
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Создан")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Обновлен")
    )

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text[:50]}..."

    def get_accuracy_rate(self):
        """Возвращает процент правильных ответов"""
        if self.times_asked == 0:
            return 0
        return round((self.correct_answers / self.times_asked) * 100, 1)


class GameRound(models.Model):
    """
    Раунд игры с вопросом
    """
    game_session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE,
        related_name='rounds',
        verbose_name=_("Игровая сессия")
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Вопрос")
    )
    round_number = models.PositiveIntegerField(
        verbose_name=_("Номер раунда")
    )

    # Время
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Начался")
    )
    time_limit_seconds = models.PositiveIntegerField(
        default=60,
        verbose_name=_("Время на ответ (секунды)")
    )

    class Meta:
        verbose_name = _("Раунд игры")
        verbose_name_plural = _("Раунды игры")
        unique_together = ['game_session', 'round_number']
        ordering = ['game_session', 'round_number']

    def __str__(self):
        return f"Round {self.round_number} in {self.game_session}"


class Answer(models.Model):
    """
    Ответ игрока на вопрос
    """
    player = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name=_("Игрок")
    )
    game_round = models.ForeignKey(
        GameRound,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_("Раунд игры")
    )
    answer_text = models.TextField(
        verbose_name=_("Текст ответа")
    )
    is_correct = models.BooleanField(
        verbose_name=_("Правильный ответ")
    )
    points_earned = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Заработанные очки")
    )
    answered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Время ответа")
    )

    class Meta:
        verbose_name = _("Ответ")
        verbose_name_plural = _("Ответы")
        unique_together = ['player', 'game_round']

    def __str__(self):
        return f"{self.player} -> {self.game_round}: {'✓' if self.is_correct else '✗'}"
