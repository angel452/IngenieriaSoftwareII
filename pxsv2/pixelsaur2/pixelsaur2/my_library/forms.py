from django import forms
from pixelsaurapp.models import Calificacion
class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['rating']
