from django.shortcuts import render
from .models import MyBuyedProducts, Descarga
from django.shortcuts import render, get_object_or_404, redirect
from pixelsaurapp.models import Category,Product,Calificacion 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pixelsaurapp.models import Product
from itertools import chain

from .forms import ReviewCreateForm, DownloadForm

# Create your views here.


@login_required
#seleccionamos todos los productos comprados para mostrarlos
def my_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    id_prod = MyBuyedProducts.objects.values('producto_comprado_id').filter(usuario_comprador=request.user.id)
    products = Product.objects.all().filter( id__in =id_prod )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = MyBuyedProducts.filter(category=category)
    
    return render(request, 'my_library/product/list.html',
        {'category': category, 'categories': categories, 'my_products': products, 'section': 'product_listLogin'})


#mostramos el detalle del producto, con un select en cada uno de los 
def my_product_detail(request, slug, id):
    #get object encuentra un producto o envia un 404 en la pagina
    product = get_object_or_404(Product,
                                id = id,
                                slug=slug,)
    
    categories = Category.objects.all()
    
    return render(request,
                  'my_library/product/detail.html',
                  {'product': product,'categories': categories,'slug':slug,'id':id}) #calification form


#funcion para hacer el la calificacion, encuentra el producto, el formulario numerico, y fguarda en la tabla de calificaciones
def review_product(request, id,slug):
    product = get_object_or_404(Product, id = id )
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ReviewCreateForm(request.POST)
        if form.is_valid():

            Calificacion.objects.create(product = product, user =  request.user , rating = form.cleaned_data['rating'])
            messages.success(request, 'calificacion dada correctamente')
            val = form.cleaned_data['rating']
            val_p = Product.objects.filter(id =id).values('val_promedio')
            val_p = val_p[0]['val_promedio'] 
            print(val_p)
            ###
            
            Product.objects.filter(id = id).update(val_promedio = (val_p + val)/2)
            product.promedio(val)
            
            ###
            return render(request,'my_library/product/detail.html',{'product':product,'categories':categories})
        else:
            form = ReviewCreateForm()
    else:
        form = ReviewCreateForm()
       
    return render(request,
                  'my_library/product/detail.html',
                  {'product': product,'categories': categories,'form':form, 'slug': slug, 'id': id})



#funcion para guardar los detalles de descarga, para un futuro historial de descargas
def download_file(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug)
    categories = Category.objects.all()
    link = product.get_link()
    form = DownloadForm()
    print(link)
    if request.method == 'get':
        print('into download')
        form = DownloadForm(request.POST)
        if form.is_valid():
            product.ondescarga()
            Descarga.objects.create(product=product,precio = product.get_precio_compra())
            return render(request,
                  'my_library/product/detail.html',
                  {'product': product,'categories': categories,'form':form, 'slug': slug, 'id': id, 'link':link})
        else:
            form = DownloadForm()
    else:
        form = DownloadForm()
    return render(request,
                  'my_library/product/detail.html',
                  {'product': product,'categories': categories,'form':form, 'slug': slug, 'id': id, 'link':link})

