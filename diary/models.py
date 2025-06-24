from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomField(models.Model):
    """Модель для хранения типов дополнительных полей"""
    FIELD_TYPES = [
        ('nutrition', 'Дневник питания'),
        ('sport', 'Спорт'),
        ('water', 'Вода'),
        ('snacks', 'Перекусы'),
        ('bad_habits', 'Вредные привычки'),
        ('good_habits', 'Полезные привычки'),
        ('gratitude', 'Дневник благодарности'),
        ('custom', 'Свое поле')
    ]

    name = models.CharField('Название поля', max_length=100)
    field_type = models.CharField('Тип поля', max_length=50, choices=FIELD_TYPES)
    description = models.TextField('Описание', blank=True)
    is_default = models.BooleanField('Стандартное поле', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'


class UserSelectedFields(models.Model):
    """Выбранные пользователем поля для дневника"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='selected_fields'
    )
    fields = models.ManyToManyField(
        CustomField,
        verbose_name='Выбранные поля'
    )
    custom_field_name = models.CharField(
        'Название своего поля',
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"Настройки полей для {self.user.username}"

    class Meta:
        verbose_name = 'Настройка полей пользователя'
        verbose_name_plural = 'Настройки полей пользователей'


class DiaryEntry(models.Model):
    """Основная модель записи в дневнике"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diary_entries'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    entry_text = models.TextField('Основной текст', blank=False)

    # Поля для хранения дополнительных данных в JSON
    additional_data = models.JSONField(
        'Дополнительные данные',
        default=dict,
        blank=True
    )

    def __str__(self):
        return f"Запись от {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name = 'Запись дневника'
        verbose_name_plural = 'Записи дневника'
        ordering = ['-created_at']