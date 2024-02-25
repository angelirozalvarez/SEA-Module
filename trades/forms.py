from django import forms

from trades.models import Trade


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'