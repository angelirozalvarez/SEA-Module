from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeModelForm

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

def trade_create(request):
    form = TradeModelForm()
    if request.method == 'POST':
        form = TradeModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/trades/trade-list/')
    context = {
        "form": form
    }
    return render(request, 'trades/trade_create.html', context)

def trade_update(request, pk):
    trade = Trade.objects.get(id=pk)
    form = TradeModelForm(instance=trade)
    if request.method == 'POST':
        form = TradeModelForm(request.POST, instance=trade)
        if form.is_valid():
            form.save()
            return redirect('/trades/trade-list/')
    context = {
        'form': form,
        'trade': trade
    }
    return render(request, 'trades/trade_update.html', context)

def trade_delete(request, pk):
    trade = Trade.objects.get(id=pk)
    trade.delete()
    return redirect('/trades/trade-list/')













