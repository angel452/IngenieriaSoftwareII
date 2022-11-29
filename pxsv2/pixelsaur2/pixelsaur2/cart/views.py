from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from pixelsaurapp.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


#require_POST es necesario ya que estas funciones se validan despues de enviar el formulario

#Funcion para agregar productos al carro, verificar el formulario y existencia de producto
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

#FUncion para eliminar productos del carrito
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

#FUncion para mostrar el precio de detalle despues de agregacion de descuento
def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={ 'quantity': item['quantity'], 'override': True})
    
    coupon_apply_form = CouponApplyForm()


    return render(request, 'cart/detail.html', {'cart': cart,'categories':categories, 'coupon_apply_form': coupon_apply_form})