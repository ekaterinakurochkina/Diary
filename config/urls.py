from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # Главная страница (перенаправление на дневник)
    path('', RedirectView.as_view(url='/diary/', permanent=True)),

    # Приложение diary
    path('diary/', include('diary.urls')),

    # Приложение users (авторизация)
    path('accounts/', include('users.urls')),
]

# Для работы с медиа-файлами в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Обработка 404 и 500 ошибок (опционально)
# handler404 = 'diary.views.handler404'
# handler500 = 'diary.views.handler500'

# Для сброса пароля:
urlpatterns += [
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
