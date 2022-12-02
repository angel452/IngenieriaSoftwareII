from django import forms
#funcion adicional para limitar la cantidad de compras de un producto
#extension extra en caso de que se pueda comprar para mas cantidad de un producto
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 2)]


#formulario para sumar al carrito despues de navegar en la vista de productos lista
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)