from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    display_name = forms.CharField(
        label='Как к вам обращаться?',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя или псевдоним'})
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'})
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Не менее 8 символов'})
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('email', 'display_name', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'})
    )

    error_messages = {
        'invalid_login': "Неверный email или пароль",
        'inactive': "Этот аккаунт неактивен",
    }
