from django.urls import path
from .views import TraderListView, TraderDetailView, TraderCreateView, TraderUpdateView, deleteTrader

app_name = 'traders'

urlpatterns = [
    path('trader-list/', TraderListView.as_view(), name='trader-list'),
    path('trader-detail/<int:pk>/', TraderDetailView.as_view(), name='trader-detail'),
    path('trader-update/<int:pk>/', TraderUpdateView.as_view(), name='trader-update'),
    path('trader-delete/<int:pk>/', deleteTrader, name='trader-delete'),
    path('trader-create/', TraderCreateView.as_view(), name='trader-create'),
]