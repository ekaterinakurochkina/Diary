from django.db import migrations


def create_default_fields(apps, schema_editor):
    CustomField = apps.get_model('diary', 'CustomField')

    # Только одно обязательное поле
    required_field = (
        1,  # order
        'Основная запись',  # name
        'text',  # field_type
        'Основное содержание дневниковой записи',  # description
        True  # is_default
    )

    # Опциональные поля (не создаем их автоматически)
    optional_fields = [
        # (2, 'Настроение', 'select', 'Ваше текущее настроение', False),
        # (3, 'Сон', 'number', 'Продолжительность сна в часах', False),
    ]

    # Создаем только обязательное поле
    order, name, field_type, description, is_default = required_field
    CustomField.objects.get_or_create(
        name=name,
        defaults={
            'field_type': field_type,
            'description': description,
            'is_default': is_default,
            'order': order
        }
    )


def remove_default_fields(apps, schema_editor):
    CustomField = apps.get_model('diary', 'CustomField')
    # Удаляем только обязательное поле
    CustomField.objects.filter(name='Основная запись').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('diary', '0002_add_order_to_customfield'),
    ]

    operations = [
        migrations.RunPython(
            create_default_fields,
            remove_default_fields
        ),
    ]
