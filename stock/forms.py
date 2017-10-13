from django import forms

from stock.models import Product, StockEntry


class StockEntryForm(forms.Form):
    amount = forms.IntegerField(label='Quantidade', required=True)
    product = forms.ModelChoiceField(
        label='Produto', queryset=Product.objects.all(), required=True
    )

    class Meta:
        model = StockEntry
