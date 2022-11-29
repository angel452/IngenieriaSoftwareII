from django import forms
from .models import Regalo

class RegaloCreateForm(forms.ModelForm):
    
    #product = forms.CharField()
    #desc_cod = forms.CharField()
    #user_send = forms.IntegerField()
    #user_rece = forms.IntegerField()
    
    class Meta: 
        model =Regalo
        #model.product = 
        fields = ['user_rece','dedicatoria']