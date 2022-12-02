from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Regalo
from cart.forms import CartAddProductForm
from django.template import loader

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .forms import RegaloCreateForm, ViewForm, BusquedaForm, PedirDineroForm
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
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category__id__in=[c.id for c in category.get_childrens()]+[category.id])
    #print(category.get_childrens())
    forma = ViewForm()
    slides = products[:10]
    if request.method == 'POST':
        forma = ViewForm(request.POST)
        #el formulario tendra tres tipos de ordenamiento, por novedad, por calificaion, por numero de descargas
        if forma.is_valid():
            control = forma.cleaned_data.get("order")
            if control == "Nuevo": 
                products = products.order_by('created')
            elif control == "Mejor Valorados":
                products = products.order_by('val_promedio')
                #toma los 10 primeros y los manda como variables al slideshow
                slides = products[:10]
                
                cambio = []
                i = 1
                for slide in slides:
                    cambio.append(slide.get_posv() - i) 
                    slide.set_posv(i) 
                    i = i+1
                
                return render(request, 'pixelsaurapp/product/list.html', {'category': category, 'categories': categories,'cambio':cambio,'slides':slides ,'products': products, 'section': 'product_listLogin', 'regalo': regalo })
            elif control == "Mas Descargados":
                products = products.order_by('n_descarga')
                slides = products[:10]
                cambio = []
                i=1
                #toma el i para definir que cambio tuvo frente a la anterior actualizacion
                for slide in slides:
                    cambio.append(slide.get_posd() - i) 
                    slide.set_posd(i) 
                    i = i+1 
                return render(request, 'pixelsaurapp/product/list.html', {'category': category, 'categories': categories,'cambio':cambio,'slides':slides ,'products': products, 'section': 'product_listLogin', 'regalo': regalo})
    # al final muestra las variables creadas para su uso
    return render(request, 'pixelsaurapp/product/list.html',
        {'category': category, 'categories': categories, 'products': products, 'section': 'product_listLogin', 'regalo': regalo, 'slides': slides})

#funcion que usa el formulario de pedir dinero para insertarlo en la tabla de admin
def pedir_dinero(request):
    categories = Category.objects.all()
    form = PedirDineroForm()
    dinero = Wallet.objects.values('money').filter(user_id = request.user.id)
    dinero = dinero[0]['money']
    if request.method == 'POST':
        form = PedirDineroForm(request.POST)
        if form.is_valid():
            print('in buscar form')
            cantidad = form.cleaned_data['cantidad']
            #print(type(cantidad))
            #Wallet.objects.create(peticion = cantidad)
            Wallet.objects.filter(user_id = request.user.id).update(peticion = cantidad)

    return render(request, 'pixelsaurapp/balance/balancemain.html',{'categories': categories,'form':form,'dinero':dinero})



#vista que toma el formulario de busqueda para hcer un filter en los productos, tambien muestra las categorias como productos en si
def search_view(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    #condicional de categoria
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category__id__in=[c.id for c in category.get_childrens()]+[category.id])
    form = BusquedaForm()
    if request.method == 'POST':
        form = BusquedaForm(request.POST)
        if form.is_valid():
            products =  products.filter(name__contains = form.cleaned_data['busqueda'])
            return render(request, 'pixelsaurapp/busqueda/res_busqueda.html',
                {'category': category, 'categories': categories, 'products': products, 'section': 'product_listLogin'})

    return render(request, 'pixelsaurapp/busqueda/buscarlist.html',
        {'category': category, 'categories': categories, 'products': products, 'section': 'product_listLogin'})
    

#muestra el detalle del producto cuando se le hace click
def product_detail(request, slug, id):
    product = get_object_or_404(Product,
                                id = id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    categories = Category.objects.all()
    califi = Product.objects.filter(id = id).values('val_promedio')

    print(califi)
    return render(request,
                  'pixelsaurapp/product/detail.html',
                  {'product': product,
                    'slug':slug,'id':id,
                    'califi':califi,
                  'categories': categories,
                   'cart_product_form': cart_product_form})


#vista que une el formulario de regalo para que puedas ingresar el mensaje del regalo y el usuario, previamente seleccionaste el producto y validaste que tienes dinero suficiente
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
                #resta el dinero
                Wallet.objects.filter(user_id = request.user.id).update(money = dinero - product.price)
                #crea el cupon de descuento
                Coupon.objects.create(code = cod_desc, valid_from = str(datetime.now()), valid_to = str(datetime.now() + timedelta(days=3)), discount = 100, active= True)
                #lo guarda en la tabla de regalos
                Regalo.objects.create(product=product,desc_cod=cod_desc,user_send = request.user , user_rece = form.cleaned_data['user_rece'], dedicatoria = form.cleaned_data['dedicatoria'])
                
            return render(request, 'pixelsaurapp/regalo/regalocreado.html', {'categories':categories,'slug':slug,'id':id})
        else:
            print('no suficiente dinero')
            form  = RegaloCreateForm()
    else:
        print('elseif')
        form = RegaloCreateForm()
    return  render(request, 'pixelsaurapp/regalo/regalocrearform.html', { 'categories':categories,'form': form,'slug':slug,'id':id})
