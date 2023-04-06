from django import forms
from .models import Product, Inbound, Outbound


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'size', 'code', 'description', 'price']


class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product', 'quantity']


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity']
