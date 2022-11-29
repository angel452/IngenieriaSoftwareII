from django.db import models
from django.contrib.auth.models import User
import decimal

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,null=True,blank=True)

    def get_money(self):
        return self.money
    def pagar(self,costo_total):
        self.money = decimal.Decimal(self.money) - decimal.Decimal(costo_total)
    def __str__(self):
        return self.user.username