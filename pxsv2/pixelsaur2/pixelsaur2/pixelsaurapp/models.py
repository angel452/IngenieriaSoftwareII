from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from coupons.models import Coupon
from django import forms





# Create your models here.

#METODOS generales
    #meta: ordenacion de nombres a la hora de mostrarse en la web
    #get_absolute_url: ubicacion de acceso en la base de datos a pagina web
    
#tabla producto relacionado al DSV_10 del diagrama de clases,  cada uno de ellos pertenece a un atributo en orden.
class Product(models.Model):

    #category = models.ForeignKey('Category', related_name='products',on_delete=models.CASCADE)

    name = models.CharField(max_length=200,help_text="Entra el nombre de tu producto", db_index=True)
    category = TreeForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    slug = models.SlugField(max_length=200)
    usuario = models.CharField(max_length=200,help_text="Entra el nombre del autor", db_index=True)
    #usuario_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)

    description = models.TextField(max_length=1000, help_text="Entra una descripcion del contenido")
    
    price = models.DecimalField(max_digits=10,decimal_places=2,default=99.99,null=True,blank=True)
    
    image = models.ImageField(null=True, blank=True,upload_to="contenidos/%Y/%m/%d") 
    archive = models.FileField(null=True, blank=True, upload_to="contenidos/%Y/%m/%d")
    available = models.BooleanField(default=True)
    
    created=models.DateField(auto_now_add=True,null=True,blank=True)
    updated=models.DateField(auto_now=True,null=True,blank=True)
    n_descarga = models.IntegerField(default=0 ,blank=True)
    val_promedio = models.FloatField(blank=True,default=0)
    pos_valoracion = models.IntegerField(blank=True,default=9999)
    pos_descarga = models.IntegerField(default=9999,blank=True)

    def promedio(self,valor):
        self.val_promedio = (self.val_promedio +valor)/2
    #define las posiciones respecto a las anteriores, de valoracion y de descargas
    def get_posv(self):
        return self.pos_valoracion
    def get_calificaion(self):
        return self.val_promedio
    def set_posv(self, valor):
        self.pos_valoracion = valor
    def get_posd(self):
        return self.n_descarga
    def set_posd(self, valor):
        self.pos_descarga = valor
    #cada ves que descarga, suma en uno al n de descargas del producto
    def ondescarga(self):
        self.n_descarga = self.n_descarga +1
        self.save()
    
   
    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name
   
    #url para redirigir a la pagina especifica
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_detail', args=[self.id, self.slug])
    
    #url que redirecciona
    def get_downloadable_url(self):   
        return reverse('my_library:my_product_detail', args=[self.id, self.slug])
    #obtiene el link especifico del archivo, para las descargas
    def get_link(self):
        return '../../media/'+self.archive.name
    def save(self, *args, **kwargs):
      if not self.slug:
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
      super().save(*args, **kwargs)



#tabla categoria perteneciente al DSV_12 los id, son automaticos, los nombres.
class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=100, null=True, blank=True)
    #carga de libreria para poder mostrar la categoria en el administrador
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    #sobrecarga de la funcion save, que guarda los productos que nosotros deseamos
    def save(self, *args, **kwargs):
        value = self.name
        if not self.slug:
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    #funcion para obtener todos los hijos y poderlos filtrar en cada producto    
    def get_childrens(self):
        return Category.objects.filter(parent=self).all()

    #redireccion para cargar los contenidos pertenecientes a una categoria    
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_list_by_category', args=[self.slug])    



#tabla calificacion, que se redirigira a las otras tablas, la calificacion numerica y la fecha por producto
class Calificacion(models.Model):
    product = models.ForeignKey(Product,related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews',on_delete=models.CASCADE,null=True)
    rating = models.FloatField(default=3.0)
    date_rating = models.DateField(auto_now_add=True, null=True)
 
#tabla de regalo, podra ser accesada por el que envia y por el que recibe
#el que envia guarda la information en la tabla
#el que recibe busca su id y muestra los contenidos referentes a su id
class Regalo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    desc_cod = models.CharField(max_length=50,unique=True, null=True, blank=True)
    user_send = models.ForeignKey( User, null=True, blank=True, on_delete=models.CASCADE)
    user_rece = models.EmailField( null=True, blank=True)
    dedicatoria = models.TextField(null=True, blank=True, max_length=200)
    #funcion del que recibe, los mensajes que le pertenecen
    def get_mensajes(self,email):
        print(self.objects.all().filter(user_rece=email))
        return self.objects.all().filter(user_rece=email)
