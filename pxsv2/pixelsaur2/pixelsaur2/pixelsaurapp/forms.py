from django import forms
from .models import Regalo
#formulario de creacion de regalo
class RegaloCreateForm(forms.ModelForm):
    class Meta: 
        model =Regalo        
        fields = ['user_rece','dedicatoria']
class ViewForm(forms.Form):
    order = forms.CharField(max_length=40)
    
#formulario busqueda
class BusquedaForm(forms.Form):
    busqueda = forms.CharField(max_length=40)

#formulario para ingresar la cantidad de dinero deseada
class PedirDineroForm(forms.Form):
    cantidad = forms.FloatField()