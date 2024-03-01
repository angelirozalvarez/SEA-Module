from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from trades.models import Bank
from trades.forms import BankModelForm
from trades.decorators import allowed_users
from django.contrib.auth.decorators import login_required

class BankListView(LoginRequiredMixin, generic.ListView):
    template_name = 'banks/bank_list.html'
    queryset = Bank.objects.all()
    context_object_name = 'banks'


class BankCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'banks/bank_create.html'
    form_class = BankModelForm

    def get_success_url(self):
        return reverse('banks:bank-list')

    def form_valid(self, form):
        messages.success(self.request, 'Bank successfully added.')
        return super().form_valid(form)

class BankUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'banks/bank_update.html'
    queryset = Bank.objects.all()
    form_class = BankModelForm

    def get_success_url(self):
        return reverse('banks:bank-list')

    def form_valid(self, form):
        messages.success(self.request, 'Bank successfully updated.')
        return super().form_valid(form)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteBank(request, pk):
    bank = Bank.objects.get(id=pk)
    context = {
        'bank': bank
    }
    if request.method == 'POST':
        bank.delete()
        messages.success(request, 'Bank successfully deleted.')
        return redirect('banks:bank-list')

    return render(request, "banks/bank_delete.html", context)
