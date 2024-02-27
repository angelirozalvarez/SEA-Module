from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trade
from .forms import TradeModelForm, CustomUserCreationForm


def signup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created. Please login.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.info(request, 'Username OR password is incorrect.')

    context = {}
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('landing-page')


class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = 'home_page.html'

class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


class TradeListView(LoginRequiredMixin, ListView):
    template_name = 'trades/trade_list.html'
    queryset = Trade.objects.all()
    context_object_name = 'trades'


class TradeDetailView(LoginRequiredMixin, DetailView):
        template_name = 'trades/trade_detail.html'
        queryset = Trade.objects.all()
        context_object_name = 'trade'


class TradeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'trades/trade_create.html'
    form_class = TradeModelForm

    def get_success_url(self):
        return reverse('trades:trade-list')


class TradeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'trades/trade_update.html'
    queryset = Trade.objects.all()
    form_class = TradeModelForm

    def get_success_url(self):
        return reverse('trades:trade-list')


class TradeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'trades/trade_delete.html'
    queryset = Trade.objects.all()

    def get_success_url(self):
        return reverse('trades:trade-list')











