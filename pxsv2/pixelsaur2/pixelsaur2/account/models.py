from django.db import models
from django.contrib.auth.models import User
import decimal
from django.conf import settings

# MOdelo billetera, esta es una extension al modelo de usuario, pero no por foreign key,como si fuera parte del modelo original, con una seccion de billetera
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    peticion = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0.00)
    
    #getters y setters de la billetera
    def get_money(self):
        return self.money

    def set_money(self,cantidad):
        self.money = self.money+cantidad
    

    #funcion de pagar con un argumento de dinero actual y dinero a restar despues de una compra
    def pagar(self,money_v,costo_total):
        self.money = money_v - decimal.Decimal(costo_total)
    
    def __str__(self):
        return self.user.username

# Model of Edit Profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #can be (User?, on delete...)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True);

def __str__(self):
    return f'Profile for user {self.user.username}'