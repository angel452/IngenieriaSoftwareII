from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Regalo
from cart.forms import CartAddProductForm
from django.template import loader

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .forms import RegaloCreateForm
from django.views import generic
from account.models import Wallet
from coupons.models import Coupon
from datetime import datetime, date, timedelta
#for Login
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from account.models import Wallet
#from .forms import LoginForm

#muestra una lista de productos por categoria
@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    regalo = Regalo(request)
    regalo = Regalo.objects.all().filter(user_rece=request.user.email)
    #condicional de categoria
    """#if method == 'POST
    if form.cleaned_data.get('opcion') = 'calificacion:
        products = select from products order by prod calificacion. top 10
        versionanterior = select from product_versionanterior

        for item in produc
        
        i = 1
        for item in query:
            item.orden = i
            i++
        if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        #print(category.get_childrens())
        products = Product.objects.filter(category__id__in=[c.id for c in category.get_childrens()]+[category.id])
    else if form.cleaned_data.get('opcion') = descargas:
        products = select from products order by prod n_descargas top 10
        i = 1
        for item in products:
            item.posn_descargas = i
            i++
        if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        #print(category.get_childrens())
        products = Product.objects.filter(category__id__in=[c.id for c in category.get_childrens()]+[category.id])

    return render(request, 'pixelsaurapp/product/list.html',
        {'category': category, 'categories': categories, 'products': products, 'section': 'product_listLogin', 'regalo': regalo})
        

    '"""
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        #print(category.get_childrens())
        products = Product.objects.filter(category__id__in=[c.id for c in category.get_childrens()]+[category.id])

    return render(request, 'pixelsaurapp/product/list.html',
        {'category': category, 'categories': categories, 'products': products, 'section': 'product_listLogin', 'regalo': regalo})



#muestra el detalle del producto cuando se le hace click
def product_detail(request, slug, id):
    #print('gaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    #print(Product.objects.values('archive').filter(id=id))
    product = get_object_or_404(Product,
                                id = id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    categories = Category.objects.all()

    #print('product_detailfunctional')
    return render(request,
                  'pixelsaurapp/product/detail.html',
                  {'product': product,
                    'slug':slug,'id':id,
                  'categories': categories,
                   'cart_product_form': cart_product_form})

def form_regalo(request,slug,id):
    wallett = Wallet(request)
    product = get_object_or_404(Product,id =id,slug=slug)
    categories = Category.objects.all()
    dinero = Wallet.objects.values('money').filter(user_id = request.user.id)
    dinero = dinero[0]['money']
   
    cod_desc = str(id)+slug
    #cod_desc = Product.objects.values('id')+Product.objects.values('slug')
    if request.method == 'POST':
        
        
        if product.price <= dinero:
            form = RegaloCreateForm(request.POST)
           
            if form.is_valid():
                wallett.pagar(product.price)
                Regalo.objects.create(product=product,desc_cod=cod_desc,user_send = request.user , user_rece = form.cleaned_data['user_rece'], dedicatoria = form.cleaned_data['dedicatoria'])
                
                Coupon.objects.create(code = cod_desc, valid_from = str(datetime.now()), valid_to = str(datetime.now() + timedelta(days=3)), discount = 100, active= True)
            return render(request, 'pixelsaurapp/regalo/regalocreado.html', {'categories':categories,'slug':slug,'id':id})
        else:
            print('no suficiente dinero')
            form  = RegaloCreateForm()
    else:
        print('elseif')
        form = RegaloCreateForm()
    return  render(request, 'pixelsaurapp/regalo/regalocrearform.html', { 'categories':categories,'form': form,'slug':slug,'id':id})

"""
def form_regalo(request,slug,id):
    categories = Category.objects.all()
    product = Product(request)
    #form = RegaloCreateForm(request.POST)
    return  render(request, 'pixelsaurapp/regalo/regalocrearform.html', { 'categories':categories,'product':product,'slug':slug,'id':id})
"""
    