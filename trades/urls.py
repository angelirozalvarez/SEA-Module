from django.urls import path
from .views import trade_list, trade_detail

app_name = 'trades'

urlpatterns = [
    path('trade-list/', trade_list, name='trade-list'),
    path('<pk>/', trade_detail, name='trade-detail')
]
