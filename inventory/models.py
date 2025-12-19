from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import TelegramUser


class Item(models.Model):
    """
    Предмет/вещь в игре
    """
    RARITY_CHOICES = [
        ('common', _('Обычный')),
        ('uncommon', _('Необычный')),
        ('rare', _('Редкий')),
        ('epic', _('Эпический')),
        ('legendary', _('Легендарный')),
    ]

    ITEM_TYPE_CHOICES = [
        ('consumable', _('Расходуемый')),
        ('equipment', _('Экипировка')),
        ('collectible', _('Коллекционный')),
        ('currency', _('Валюта')),
        ('other', _('Другое')),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name=_("Название предмета")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Описание")
    )
    rarity = models.CharField(
        max_length=20,
        choices=RARITY_CHOICES,
        default='common',
        verbose_name=_("Редкость")
    )
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPE_CHOICES,
        default='other',
        verbose_name=_("Тип предмета")
    )

    # Стоимость
    coin_cost = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Стоимость в монетах")
    )
    gold_cost = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Стоимость в золоте")
    )

    # Свойства предмета
    max_stack = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Максимум в стопке"),
        help_text=_("Максимальное количество предметов в одной ячейке")
    )
    is_stackable = models.BooleanField(
        default=True,
        verbose_name=_("Можно складывать"),
        help_text=_("Можно ли складывать несколько предметов в одну ячейку")
    )

    # Статус
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активен"),
        help_text=_("Доступен ли предмет для получения")
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
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()})"


class InventoryItem(models.Model):
    """
    Предмет в инвентаре игрока
    """
    player = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='inventory_items',
        verbose_name=_("Игрок")
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name=_("Предмет")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Количество")
    )

    # Дополнительные свойства для конкретного предмета
    # (можно расширить для уникальных модификаторов)

    # Когда получен предмет
    acquired_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Получен")
    )

    class Meta:
        verbose_name = _("Предмет в инвентаре")
        verbose_name_plural = _("Предметы в инвентаре")
        unique_together = ['player', 'item']  # Один тип предмета - одна запись
        ordering = ['-acquired_at']

    def __str__(self):
        return f"{self.player.username_telegram or self.player.telegram_id}: {self.item.name} x{self.quantity}"

    def add_quantity(self, amount):
        """Добавить количество предметов"""
        if self.item.is_stackable and self.quantity + amount <= self.item.max_stack:
            self.quantity += amount
            self.save()
            return True
        return False

    def remove_quantity(self, amount):
        """Убрать количество предметов"""
        if self.quantity >= amount:
            self.quantity -= amount
            if self.quantity <= 0:
                self.delete()
            else:
                self.save()
            return True
        return False
