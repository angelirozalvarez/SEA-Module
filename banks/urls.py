from django.urls import path
from .views import BankListView, BankCreateView, BankUpdateView, deleteBank

app_name = 'banks'

urlpatterns = [
    path('bank-list/', BankListView.as_view(), name='bank-list'),
    path('bank-update/<int:pk>/', BankUpdateView.as_view(), name='bank-update'),
    path('bank-delete/<int:pk>/', deleteBank, name='bank-delete'),
    path('bank-create/', BankCreateView.as_view(), name='bank-create'),
]