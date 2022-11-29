from django.db import models
from pixelsaurapp.models import Category,Product
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User  
from orders.models import Order,OrderItem
from django.utils.text import slugify
from django.urls import reverse 
# Create your models here.
class MyBuyedProducts(models.Model):
    

    #category = models.ForeignKey('Category', related_name='products',on_delete=models.CASCADE)

    #name = models.CharField(max_length=200,help_text="Entra el nombre de tu producto", db_index=True)
    #category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    #slug = models.SlugField(max_length=200)

    #usuario_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    usuario_comprador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,db_index=True)
    producto_comprado = models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True,blank=True,db_index = True)
    #description = models.TextField(max_length=1000, help_text="Entra una descripcion del contenido")
    
    #price = models.DecimalField(max_digits=10,decimal_places=2,default=99.99,null=True,blank=True)
    def get_id_comprador(self):
      return self.usuario_comprador
    #image = models.ImageField(null=True, blank=True,upload_to="contenidos/%Y/%m/%d") 
    #created=models.DateField(auto_now_add=True,null=True,blank=True)
    #ordenid = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True,blank=True)
    #valid_download = models.BooleanField(default=False)
    # file filefield
    """class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('my_library:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
      if not self.slug:
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
      super().save(*args, **kwargs)
    """



