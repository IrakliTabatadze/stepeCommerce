from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'd-flex justify-content-center'})
        }