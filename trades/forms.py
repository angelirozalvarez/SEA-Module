from django import forms

from trades.models import Trade


class TradeModelForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'