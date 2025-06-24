# from django.contrib.auth import get_user_model
#
# import admin
# from .models import CustomField, UserSelectedFields, DiaryEntry
#
# User = get_user_model()
#
#
# # Модель CustomField - только для суперпользователя
# @admin.register(CustomField)
# class CustomFieldAdmin(admin.ModelAdmin):
#     list_display = ('name', 'field_type', 'is_default', 'order')
#     list_filter = ('name')
#     search_fields = ('name')
#
#
# # Модель UserSelectedFields - только просмотр для администраторов
# @admin.register(UserSelectedFields)
# class UserSelectedFieldsAdmin(admin.ModelAdmin):
#     list_display = ('user_email', 'fields_list')
#     list_filter = ('user_email')
#     search_fields = ('user_email')
#
#
# # Модель DiaryEntry - только для суперпользователя
# @admin.register(DiaryEntry)
# class DiaryEntryAdmin(admin.ModelAdmin):
#     list_display = ('user_email', 'created_at', 'entry_preview')
#     list_filter = ('user_email')
#     search_fields = ('user_email', 'created_at')

from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomField, UserSelectedFields, DiaryEntry

User = get_user_model()


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'is_default', 'order')
    list_filter = ('field_type', 'is_default')
    search_fields = ('name',)
    list_editable = ('order', 'is_default')
    ordering = ('order', 'name')


@admin.register(UserSelectedFields)
class UserSelectedFieldsAdmin(admin.ModelAdmin):
    list_display = ('user', 'custom_field_name', 'selected_fields_list')
    filter_horizontal = ('fields',)

    def selected_fields_list(self, obj):
        return ", ".join([field.name for field in obj.fields.all()])

    selected_fields_list.short_description = 'Выбранные поля'


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_date', 'entry_preview')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    def created_date(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    created_date.short_description = 'Создано'

    def entry_preview(self, obj):
        return obj.entry_text[:50] + '...' if len(obj.entry_text) > 50 else obj.entry_text

    entry_preview.short_description = 'Запись'