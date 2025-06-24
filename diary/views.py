from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import DiaryEntry, CustomField, UserSelectedFields
from .forms import DiaryEntryForm


class DiaryEntryListView(LoginRequiredMixin, ListView):
    """Список записей дневника"""
    model = DiaryEntry
    template_name = 'diary/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_fields'] = self.request.user.diary_fields_settings.get_available_fields()
        return context


class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
    """Создание новой записи"""
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Запись успешно создана!')
        return super().form_valid(form)


class DiaryEntryUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование записи"""
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('diary:entry-list')

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена!')
        return super().form_valid(form)


class DiaryEntryDetailView(LoginRequiredMixin, DetailView):
    """Просмотр записи"""
    model = DiaryEntry
    template_name = 'diary/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_fields'] = self.request.user.diary_fields_settings.get_available_fields()
        return context


class DiaryEntryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление записи"""
    model = DiaryEntry
    template_name = 'diary/entry_confirm_delete.html'
    success_url = reverse_lazy('diary:entry-list')

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена!')
        return super().delete(request, *args, **kwargs)


class DiarySettingsView(LoginRequiredMixin, UpdateView):
    """ Настройки полей дневника """
    model = UserSelectedFields
    template_name = 'diary/settings.html'
    fields = ['fields', 'custom_field_name']
    success_url = reverse_lazy('diary:settings')

    def get_object(self):
        obj, created = UserSelectedFields.objects.get_or_create(user=self.request.user)
        if created:
            obj.fields.add(*CustomField.objects.filter(is_default=True))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_fields'] = self.object.get_available_fields()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Настройки успешно сохранены!')
        return super().form_valid(form)