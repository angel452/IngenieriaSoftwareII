from django import forms


#formulario para aplicar el cupon, tiene una oracion con el codigo de descuento
class CouponApplyForm(forms.Form):
    code= forms.CharField()