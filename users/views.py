from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView

from .forms import UserLoginForm
from .forms import UserRegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('diary:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.display_name}!')
        return response


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f'Рады снова видеть, {self.request.user.display_name}!')
        return super().get_success_url()

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect('diary:home')
        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы успешно вышли из системы')
        return super().dispatch(request, *args, **kwargs)


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete_account.html'
    success_url = reverse_lazy('users:login')

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        user = authenticate(email=request.user.email, password=password)

        if user is not None:
            messages.success(request, 'Ваш аккаунт был успешно удален')
            return super().post(request, *args, **kwargs)

        messages.error(request, 'Неверный пароль')
        return self.get(request, *args, **kwargs)
