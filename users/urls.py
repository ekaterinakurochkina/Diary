from django.urls import path
from .views import  DeleteAccountView, UserListView, UserCreateView, logout_view
from django.contrib.auth.views import LoginView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(template_name="register.html"), name='register'),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete/', DeleteAccountView.as_view(template_name="user_confirm_delete.html"), name='delete'),
    path('', UserListView.as_view(), name='home')
]
