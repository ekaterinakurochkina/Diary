from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class CustomField(models.Model):
    """Модель для хранения типов дополнительных полей"""
    FIELD_TYPES = [
        ('text', 'Текст'),
        ('number', 'Число'),
        ('checkbox', 'Галочка'),
        ('select', 'Выбор из списка'),
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
    order = models.PositiveSmallIntegerField(
        'Порядок сортировки',
        default=0,
        help_text="Число для определения порядка полей (меньше - выше)"
    )

    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()})"

    class Meta:
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'
        ordering = ['order', 'name']


class UserSelectedFields(models.Model):
    """Выбранные пользователем поля для дневника"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='selected_fields'
    )
    fields = models.ManyToManyField(
        CustomField,
        verbose_name='Выбранные поля',
        blank=True
    )
    custom_field_name = models.CharField(
        'Название своего поля',
        max_length=100,
        blank=True
    )

    def get_all_fields(self):
        """Возвращает все поля (стандартные + выбранные)"""
        return CustomField.objects.filter(
            models.Q(is_default=True) | models.Q(id__in=self.fields.all())
        ).distinct().order_by('order', 'name')

    def __str__(self):
        return f"Настройки полей для {self.user.email}"

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
    entry_text = models.TextField('Основной текст')

    additional_data = models.JSONField(
        'Дополнительные данные',
        default=dict,
        blank=True
    )

    def get_field_value(self, field_name):
        """Возвращает значение дополнительного поля"""
        return