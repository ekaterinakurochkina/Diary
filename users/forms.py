from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Пароль должен содержать минимум 8 символов"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'display_name', 'password1', 'password2')
        labels = {
            'email': 'Email',
            'display_name': 'Как к вам обращаться?'
        }
        help_texts = {
            'email': 'Это будет использоваться для входа',
            'display_name': 'Ваше имя или псевдоним для отображения'
        }
