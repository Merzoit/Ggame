from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import TelegramUser
import random


class CardTemplate(models.Model):
    """
    Шаблон карты с базовыми характеристиками
    """

    RARITY_CHOICES = [
        ('common', _('Обычная')),
        ('rare', _('Редкая')),
        ('epic', _('Эпическая')),
        ('legendary', _('Легендарная')),
        ('mythic', _('Мифическая')),
    ]

    ELEMENT_CHOICES = [
        ('fire', _('Огонь')),
        ('water', _('Вода')),
        ('earth', _('Земля')),
        ('air', _('Воздух')),
        ('light', _('Свет')),
        ('dark', _('Тьма')),
        ('neutral', _('Нейтральная')),
    ]

    # Основная информация
    name = models.CharField(
        max_length=100,
        verbose_name=_("Название карты")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Описание")
    )
    image_url = models.URLField(
        blank=True,
        verbose_name=_("URL изображения")
    )

    # Принадлежность
    anime_universe = models.CharField(
        max_length=100,
        verbose_name=_("Аниме-вселенная"),
        help_text=_("Название аниме или франшизы")
    )
    season = models.CharField(
        max_length=50,
        verbose_name=_("Сезон"),
        help_text=_("Сезон или арка аниме")
    )

    # Характеристики
    rarity = models.CharField(
        max_length=20,
        choices=RARITY_CHOICES,
        default='common',
        verbose_name=_("Редкость")
    )
    element = models.CharField(
        max_length=20,
        choices=ELEMENT_CHOICES,
        default='neutral',
        verbose_name=_("Стихия")
    )

    # Диапазоны характеристик (для генерации случайных значений)
    health_min = models.PositiveIntegerField(
        default=100,
        verbose_name=_("Мин. здоровье")
    )
    health_max = models.PositiveIntegerField(
        default=100,
        verbose_name=_("Макс. здоровье")
    )
    attack_min = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Мин. атака")
    )
    attack_max = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Макс. атака")
    )
    defense_min = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Мин. защита")
    )
    defense_max = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Макс. защита")
    )

    # Стоимость
    coin_cost = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Стоимость в монетах")
    )
    gold_cost = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Стоимость в золоте")
    )

    # Статус
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активна"),
        help_text=_("Доступна ли карта для получения")
    )

    # Мета
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Создана")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Обновлена")
    )

    class Meta:
        verbose_name = _("Шаблон карты")
        verbose_name_plural = _("Шаблоны карт")
        ordering = ['-created_at']
        unique_together = ['name', 'anime_universe', 'season']

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()}) - {self.anime_universe}"

    def get_average_stats(self):
        """Возвращает средние значения характеристик"""
        return {
            'health': (self.health_min + self.health_max) // 2,
            'attack': (self.attack_min + self.attack_max) // 2,
            'defense': (self.defense_min + self.defense_max) // 2,
        }


class CardInstance(models.Model):
    """
    Конкретный экземпляр карты у игрока со случайными характеристиками
    """

    # Связи
    template = models.ForeignKey(
        CardTemplate,
        on_delete=models.CASCADE,
        verbose_name=_("Шаблон карты")
    )
    owner = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='card_instances',
        verbose_name=_("Владелец")
    )

    # Случайные характеристики (генерируются при создании)
    health = models.PositiveIntegerField(
        verbose_name=_("Здоровье")
    )
    attack = models.PositiveIntegerField(
        verbose_name=_("Атака")
    )
    defense = models.PositiveIntegerField(
        verbose_name=_("Защита")
    )

    # Текущие значения в бою (могут изменяться)
    current_health = models.PositiveIntegerField(
        verbose_name=_("Текущее здоровье")
    )

    # Статус
    is_in_deck = models.BooleanField(
        default=False,
        verbose_name=_("В колоде"),
        help_text=_("Используется ли карта в текущей колоде игрока")
    )
    level = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Уровень")
    )
    experience = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Опыт")
    )

    # Время
    acquired_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Получена")
    )
    last_used = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Последнее использование")
    )

    class Meta:
        verbose_name = _("Карта игрока")
        verbose_name_plural = _("Карты игроков")
        ordering = ['-acquired_at']

    def __str__(self):
        return f"{self.template.name} ({self.owner.username_telegram or self.owner.telegram_id})"

    def save(self, *args, **kwargs):
        # При первом сохранении генерируем случайные характеристики
        if not self.pk:
            self.generate_random_stats()
            self.current_health = self.health
        super().save(*args, **kwargs)

    def generate_random_stats(self):
        """Генерирует случайные характеристики в заданном диапазоне"""
        template = self.template
        self.health = random.randint(template.health_min, template.health_max)
        self.attack = random.randint(template.attack_min, template.attack_max)
        self.defense = random.randint(template.defense_min, template.defense_max)

    def regenerate_stats(self):
        """Перегенерирует характеристики (для специальных случаев)"""
        self.generate_random_stats()
        self.current_health = self.health
        self.save()

    def take_damage(self, damage):
        """Получить урон"""
        actual_damage = max(0, damage - self.defense)
        self.current_health = max(0, self.current_health - actual_damage)
        self.save()
        return actual_damage

    def heal(self, amount):
        """Восстановить здоровье"""
        old_health = self.current_health
        self.current_health = min(self.health, self.current_health + amount)
        healed = self.current_health - old_health
        self.save()
        return healed

    def is_alive(self):
        """Проверка, жива ли карта"""
        return self.current_health > 0

    def reset_health(self):
        """Восстановить полное здоровье"""
        self.current_health = self.health
        self.save()
