from django import forms
from leads.models import Lead, Product

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'unit_price',
            'product_category',
        )
