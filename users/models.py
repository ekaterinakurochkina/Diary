from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите Ваш email"
    )

    display_name = models.CharField(
        max_length=150,
        verbose_name="Имя для отображения",
        help_text="Как мы будем к вам обращаться",
        validators=[
            RegexValidator(
                regex='^[a-zA-Zа-яА-ЯёЁ0-9_ ]+$',
                message='Имя может содержать только буквы, цифры и пробелы'
            )
        ]
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона"
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text='Загрузите свой аватар'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name"]  # Теперь обязательное поле при createsuperuser

    def __str__(self):
        return f"{self.display_name} ({self.email})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']