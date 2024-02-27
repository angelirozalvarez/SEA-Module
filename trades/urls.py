from django.urls import path
from .views import TradeListView, TradeDetailView, TradeCreateView, TradeUpdateView, TradeDeleteView

app_name = 'trades'

urlpatterns = [
    path('trade-list/', TradeListView.as_view(), name='trade-list'),
    path('trade-detail/<int:pk>/', TradeDetailView.as_view(), name='trade-detail'),
    path('trade-update/<int:pk>/', TradeUpdateView.as_view(), name='trade-update'),
    path('trade-delete/<int:pk>/', TradeDeleteView.as_view(), name='trade-delete'),
    path('trade-create/', TradeCreateView.as_view(), name='trade-create'),
]
