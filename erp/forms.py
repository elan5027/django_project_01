from django import forms
from .models import Product, Inbound, Outbound, CategorySize, Category




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'size', 'description', 'price']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']


class CategorySizeForm(forms.ModelForm):
    class Meta:
        model = CategorySize
        fields = ['category','size']



class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product', 'quantity']


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity']
