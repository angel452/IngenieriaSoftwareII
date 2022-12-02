from django import forms
from .models import Order


#formulario para crear los datos de compra
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']