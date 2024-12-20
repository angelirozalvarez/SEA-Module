from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from trades.models import Trade, Trader, Bank


class TradeModelForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'


class TraderModelForm(forms.ModelForm):
    class Meta:
        model = Trader
        fields = '__all__'

class BankModelForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']