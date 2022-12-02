from django.shortcuts import render
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
import decimal

from cart.cart import Cart
from django.contrib.auth.models import User
from my_library.models import MyBuyedProducts
from pixelsaurapp.models import Category
from account.models import Wallet

#funcion para colocar la orden en la tabla de ordenes, llamamos a los html donde mostrara 'created' 
# si se cumplio la funcion (si ya se hizo POST)
def order_create(request):
    cart = Cart(request)
    wallett = Wallet(request)
    categories = Category.objects.all()
    
    dinero = Wallet.objects.values('money').filter(user_id = request.user.id)
    dinero = dinero[0]['money']
   
    if request.method == 'POST':
        if cart.get_total_price_after_discount() < dinero:    
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                
                Wallet.objects.filter(user_id = request.user.id).update(money = dinero - cart.get_total_price_after_discount())

                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                for item in cart:
                    MyBuyedProducts.objects.create(usuario_comprador = request.user, producto_comprado=item['product'])
                cart.clear()
                return render(request,'orders/order/created.html', {'order': order,'categories':categories})
        else:
            print('no se pudo crear la orden, no hay dinero')
            form = OrderCreateForm()
            #return vuelta a la pagina
    else:
        form = OrderCreateForm()
    #cuando entra al if de menor diner, hacer un return de te falta dinero crac, o mandar el formulario de pedir money
    return render(request, 'orders/order/create.html', {'cart': cart, 'categories':categories,'form': form})