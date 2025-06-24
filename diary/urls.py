from django.urls import path
from .views import get_random_phrase
from .views import (
    DiaryEntryListView, DiaryEntryCreateView,
    DiaryEntryUpdateView, DiaryEntryDetailView,
    DiaryEntryDeleteView, DiarySettingsView
)

app_name = 'diary'

urlpatterns = [
    path('', DiaryEntryListView.as_view(), name='entry-list'),
    path('create/', DiaryEntryCreateView.as_view(), name='entry-create'),
    path('<int:pk>/', DiaryEntryDetailView.as_view(), name='entry-detail'),
    path('<int:pk>/update/', DiaryEntryUpdateView.as_view(), name='entry-update'),
    path('<int:pk>/delete/', DiaryEntryDeleteView.as_view(), name='entry-delete'),
    path('settings/', DiarySettingsView.as_view(), name='settings'),
    path('get-random-phrase/', get_random_phrase, name='get-random-phrase'),
]