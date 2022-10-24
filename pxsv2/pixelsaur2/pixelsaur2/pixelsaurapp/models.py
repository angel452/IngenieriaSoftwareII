from django.db import models
from django.contrib.auth.models import User  # Required to assign User as a borrower

# Create your models here.
class contenido(models.Model):
    #nombre del contenido
    name = models.CharField(max_length=200,help_text="Entra el nombre de tu producto", null=True, blank=True)
    #conseguimos el nombre del autor (no confirmado)
    usuario_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    #description del contenido
    descripcion = models.TextField(max_length=1000, help_text="Entra una descripcion del contenido")
    
    precio = models.DecimalField(max_digits=100,decimal_places=2,default=99.99,null=True,blank=True)
    #obten el nombre por foreign key de la categoria (no confirmado)
    id_categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True)
    #ver si sube media (no confirmado)
    media_banner = models.ImageField(null=True, blank=True,upload_to="images/") 
    #poner la promocion por tiempo
    promocion = models.DecimalField(max_digits=100, decimal_places=2, default=99.99, null=True, blank=True)
    #dependiendo a esta fecha
    fecha_inicio=models.DateField(null=True,blank=True)
    fecha_fin=models.DateField(null=True,blank=True)

    class Meta:
        ordering = ['name']



    def __str__(self):
        return self.name

class Categoria(models.Model):
    nombre = models.CharField(max_length=100,help_text="Nombre de la categoria")
    class Meta:
        ordering = ['nombre']
    def __str__(self):
        return self.nombre
class downloadInstance(models.Model):
    