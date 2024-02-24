from django.shortcuts import render
from django.http import HttpResponse
from .models import Trade

def trade_list(request):
    trades = Trade.objects.all()
    context = {
        'trades': trades
    }
    return render(request, 'trades/trade_list.html', context)

def trade_detail(request, pk):
    trade = Trade.objects.get(id=pk)
    context = {
        'trade': trade
    }
    return render(request, 'trades/trade_detail.html', context)