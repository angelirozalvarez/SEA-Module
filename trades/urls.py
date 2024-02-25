from django.urls import path
from .views import trade_list, trade_detail, trade_create, trade_update, trade_delete

app_name = 'trades'

urlpatterns = [
    path('trade-list/', trade_list, name='trade-list'),
    path('trade-detail/<int:pk>/', trade_detail, name='trade-detail'),
    path('trade-update/<int:pk>/', trade_update, name='trade-update'),
    path('trade-delete/<int:pk>/', trade_delete, name='trade-delete'),
    path('trade-create/', trade_create, name='trade-create'),
]
