from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserRegisterForm


class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    list_display = ('email', 'display_name', 'is_active', 'is_staff')
    search_fields = ('email', 'display_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('display_name', 'phone', 'avatar')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'display_name', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)