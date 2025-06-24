from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Кастомизированная админка для пользователей
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'display_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_staff=True)  # Админы видят только staff пользователей

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
