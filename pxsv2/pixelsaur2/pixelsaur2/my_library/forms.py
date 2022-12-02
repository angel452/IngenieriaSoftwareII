from django import forms
from pixelsaurapp.models import Calificacion



#formulario para recibir la cantidad numerica en la calificacion, de nombre rating
class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['rating']

#formulario para guardar los datos cuando hace la descarga ()fecha, nombre de usuario, precio)
class DownloadForm(forms.Form):
    
    nombre = forms.CharField(max_length=40)
    precio = forms.FloatField()