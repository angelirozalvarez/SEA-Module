from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Trade
from .forms import TradeModelForm, CustomUserCreationForm
from .decorators import unauthenticated_user, allowed_users


User = get_user_model()

@unauthenticated_user
def adminSignup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Set user as staff
            user.is_superuser = True  # Set user as superuser
            user.save()

            admin_group, created = Group.objects.get_or_create(name='Admin')
            user.groups.add(admin_group)

            messages.success(request, 'Admin account successfully created. Please login.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/admin_signup.html', context)

@unauthenticated_user
def regularUserSignup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='Regular User')
            user.groups.add(group)

            messages.success(request, 'Regular user account successfully created. Please login.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/regular_user_signup.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, 'Username OR password is incorrect.')

    context = {}
    return render(request, 'registration/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('landing-page')


class LogoutConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/confirm_logout.html'


class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = 'home_page.html'


class UnauthorisedMessageView(LoginRequiredMixin, TemplateView):
    template_name = 'unauthorised_message.html'

@unauthenticated_user
def landingPage(request):
    return render(request, 'landing_page.html')


@unauthenticated_user
def signupOptionPage(request):
    return render(request, 'registration/signup_option.html')

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

    def form_valid(self, form):
        messages.success(self.request, 'Trade successfully created.')
        return super().form_valid(form)

class TradeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'trades/trade_update.html'
    queryset = Trade.objects.all()
    form_class = TradeModelForm

    def get_success_url(self):
        return reverse('trades:trade-list')

    def form_valid(self, form):
        messages.success(self.request, 'Trade successfully updated.')
        return super().form_valid(form)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def deleteTrade(request, pk):
    trade = Trade.objects.get(id=pk)
    context = {
        'trade': trade
    }
    if request.method == 'POST':
        trade.delete()
        messages.success(request, 'Trade successfully deleted.')
        return redirect('trades:trade-list')

    return render(request, "trades/trade_delete.html", context)
