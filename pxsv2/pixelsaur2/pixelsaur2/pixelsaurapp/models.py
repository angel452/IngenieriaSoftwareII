from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User  # Required to assign User as a borrower
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from coupons.models import Coupon
from django import forms


"""
class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    #first_name = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    #last_name = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length = 254)
    money = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,null=True,blank=True)
    password    =   models.CharField(max_length=20, widget=forms.PasswordInput)
    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    def __str__(self):
        return "{}".format(self.email)   
#     money = models.DecimalField(max_digits = 10, decimal_places = 2, default=0, null=True, blank = True)
"""


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
    n_descarga = models.IntegerField(null=True, blank=True)
    val_promedio = models.FloatField(blank=True,null = True)
    pos_valoracion = models.IntegerField(blank=True,null = True)
    pos_descarga = models.IntegerField(null = True,blank=True)

    def ondescarga(self):
        self.n_descarga = self.n_descarga + 1
    def promedio(self,valor):
        self.val_promedio = (self.val_promedio +valor)/2
    
    
    #valid download = false
    #file = file
    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name
    #def is_downloadavle(self):
    #   return available.
    
    def get_absolute_url(self):
        #print('is this the path?')

        return reverse('pixelsaurapp:product_detail', args=[self.id, self.slug])
    def get_downloadable_url(self):
        #print('is this the path?')
        return reverse('my_library:my_product_detail', args=[self.id, self.slug])
    def get_link(self):
        print('gaaaaaaa')
        print(self.archive.name)
        return '../../media/'+self.archive.name
    def save(self, *args, **kwargs):
      if not self.slug:
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
      super().save(*args, **kwargs)

#tabla categoria perteneciente al DSV_12 los id, son automaticos, los nombres.
"""
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
"""

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=100, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        if not self.slug:
            self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    def get_childrens(self):
        return Category.objects.filter(parent=self).all()
    def get_absolute_url(self):
        return reverse('pixelsaurapp:product_list_by_category', args=[self.slug])    

class Calificacion(models.Model):
    product = models.ForeignKey(Product,related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews',on_delete=models.CASCADE,null=True)
    rating = models.FloatField(default=3.0)
    date_rating = models.DateField(auto_now_add=True, null=True)
    #def get_absolute_url(self):
    #    return self.product.get_absolute_url()

class Regalo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)
    desc_cod = models.CharField(max_length=50,unique=True, null=True, blank=True)
    user_send = models.ForeignKey( User, null=True, blank=True, on_delete=models.CASCADE)
    user_rece = models.EmailField( null=True, blank=True)
    dedicatoria = models.TextField(null=True, blank=True, max_length=200)

    def get_mensajes(self,email):
        print(self.objects.all().filter(user_rece=email))
        return self.objects.all().filter(user_rece=email)
