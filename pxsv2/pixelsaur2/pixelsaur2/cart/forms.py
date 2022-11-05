from django import forms
#funcion adicional para limitar la cantidad de compras de un producto
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 2)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)