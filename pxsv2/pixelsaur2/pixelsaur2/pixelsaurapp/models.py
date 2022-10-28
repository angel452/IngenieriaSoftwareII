from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User  # Required to assign User as a borrower
# Create your models here.


class Product(models.Model):
    #obten el
    #  nombre por foreign key de la categoria (no confirmado)
    category = models.ForeignKey('Category', related_name='products',on_delete=models.CASCADE)
    #nombre del contenido
    name = models.CharField(max_length=200,help_text="Entra el nombre de tu producto", db_index=True)
    
    slug = models.SlugField(max_length=200,db_index=True)
    #conseguimos el nombre del autor (no confirmado)
    usuario_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    #description del contenido
    description = models.TextField(max_length=1000, help_text="Entra una descripcion del contenido")
    
    price = models.DecimalField(max_digits=10,decimal_places=2,default=99.99,null=True,blank=True)
    #ver si sube media (no confirmado)
    image = models.ImageField(null=True, blank=True,upload_to="contenidos/%Y/%m/%d") 
    #poner la promocion por tiempo
    #promocion = models.DecimalField(max_digits=10, decimal_places=2, default=99.99, null=True, blank=True)
    available = models.BooleanField(default=True)
    #dependiendo a esta fecha
    created=models.DateField(auto_now_add=True,null=True,blank=True)
    updated=models.DateField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_detail', args=[self.id, self.slug])

class Category(models.Model):
    #categoria_padre = models.ForeignKey(Categoria, null=True)
    name = models.CharField(max_length=100,help_text="Nombre de la categoria",db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_list_by_category', args=[self.slug])

