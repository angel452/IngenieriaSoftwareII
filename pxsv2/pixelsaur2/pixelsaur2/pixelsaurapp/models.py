from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User  # Required to assign User as a borrower
# Create your models here.

#METODOS generales
    #meta: ordenacion de nombres a la hora de mostrarse en la web
    #get_absolute_url: ubicacion de acceso en la base de datos a pagina web
    
#tabla producto relacionado al DSV_10 del diagrama de clases,  cada uno de ellos pertenece a un atributo en orden.
class Product(models.Model):

    category = models.ForeignKey('Category', related_name='products',on_delete=models.CASCADE)

    name = models.CharField(max_length=200,help_text="Entra el nombre de tu producto", db_index=True)
    
    slug = models.SlugField(max_length=200,db_index=True)

    usuario_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    description = models.TextField(max_length=1000, help_text="Entra una descripcion del contenido")
    
    price = models.DecimalField(max_digits=10,decimal_places=2,default=99.99,null=True,blank=True)
    
    image = models.ImageField(null=True, blank=True,upload_to="contenidos/%Y/%m/%d") 
   
    available = models.BooleanField(default=True)
    
    created=models.DateField(auto_now_add=True,null=True,blank=True)
    updated=models.DateField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_detail', args=[self.id, self.slug])

#tabla categoria perteneciente al DSV_12 los id, son automaticos, los nombres.
class Category(models.Model):
    
    name = models.CharField(max_length=100,help_text="Nombre de la categoria",db_index=True)
    #slug: genera un path ser tomado en las direcciones de la pagina web
    slug = models.SlugField(max_length=200,unique=True)
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_list_by_category', args=[self.slug])

