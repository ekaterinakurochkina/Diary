from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from diary.models import CustomField, UserSelectedFields

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_selected_fields(sender, instance, created, **kwargs):
    """
    Автоматически создает настройки полей для нового пользователя
    и добавляет стандартные поля
    """
    if created:
        # Создаем запись UserSelectedFields для нового пользователя
        user_fields = UserSelectedFields.objects.create(user=instance)

        # Добавляем все стандартные поля
        default_fields = CustomField.objects.filter(is_default=True)
        user_fields.fields.add(*default_fields)

        # Можно установить какое-то значение для custom_field_name
        user_fields.custom_field_name = "Мое поле"
        user_fields.save()
