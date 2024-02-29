from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from trades.models import Trader
from trades.forms import TraderModelForm
from trades.decorators import allowed_users
from django.contrib.auth.decorators import login_required

class TraderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'traders/trader_list.html'
    queryset = Trader.objects.all()
    context_object_name = 'traders'

class TraderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'traders/trader_detail.html'
    queryset = Trader.objects.all()
    context_object_name = 'trader'

class TraderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'traders/trader_create.html'
    form_class = TraderModelForm

    def get_success_url(self):
        return reverse('traders:trader-list')

    def form_valid(self, form):
        messages.success(self.request, 'Trader successfully added.')
        return super().form_valid(form)

class TraderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'traders/trader_update.html'
    queryset = Trader.objects.all()
    form_class = TraderModelForm

    def get_success_url(self):
        return reverse('traders:trader-list')

    def form_valid(self, form):
        messages.success(self.request, 'Trader successfully updated.')
        return super().form_valid(form)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteTrader(request, pk):
    trader = Trader.objects.get(id=pk)
    context = {
        'trader': trader
    }
    if request.method == 'POST':
        trader.delete()
        messages.success(request, 'Trader successfully deleted.')
        return redirect('traders:trader-list')

    return render(request, "traders/trader_delete.html", context)







