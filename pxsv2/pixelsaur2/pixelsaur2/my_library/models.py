from django.db import models
from pixelsaurapp.models import Category,Product
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User  
from orders.models import Order,OrderItem
from django.utils.text import slugify
from django.urls import reverse 
# Tabla de libreria tiene fk de usuario y sus productos que tiene, un usuario puede tener varios productos 
class MyBuyedProducts(models.Model):
    
  usuario_comprador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,db_index=True)
  producto_comprado = models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True,blank=True,db_index = True)

  def get_id_comprador(self):
    return self.usuario_comprador
    

#tabla con los contenidos de la descarga
class Descarga(models.Model):
  producto = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
  fecha = models.DateTimeField(auto_now_add=True)
  precio = models.FloatField(blank=True)