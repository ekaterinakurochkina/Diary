from django import forms
from .models import DiaryEntry


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['entry_text']
        widgets = {
            'entry_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Добавляем динамические поля
        if self.user:
            for field in self.user.diary_fields_settings.get_available_fields():
                self.fields[f'field_{field.id}'] = self.get_field_widget(field)

    def get_field_widget(self, field):
        """Возвращает соответствующий виджет для типа поля"""
        if field.field_type == 'number':
            return forms.FloatField(
                label=field.name,
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
        elif field.field_type == 'checkbox':
            return forms.BooleanField(
                label=field.name,
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
        else:  # text, select и другие
            return forms.CharField(
                label=field.name,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()
            self.save_additional_data(instance)

        return instance

    def save_additional_data(self, instance):
        """Сохраняет дополнительные данные в JSON"""
        additional_data = {}
        for field in self.user.diary_fields_settings.get_available_fields():
            field_key = f'field_{field.id}'
            if field_key in self.cleaned_data:
                additional_data[field.name] = self.cleaned_data[field_key]

        instance.additional_data = additional_data
        instance.save()
        