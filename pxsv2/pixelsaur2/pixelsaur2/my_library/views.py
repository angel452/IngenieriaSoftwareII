from django.shortcuts import render
from .models import MyBuyedProducts
from django.shortcuts import render, get_object_or_404, redirect
from pixelsaurapp.models import Category,Product,Calificacion 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pixelsaurapp.models import Product
from .forms import ReviewCreateForm

# Create your views here.


@login_required
def my_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    #myprod = MyBuyedProducts(request)
    #select products from products_list where user.id = buyed.id 
    #print('gaaaaaaaaaaaaaaaaaaaaa')
    id_prod = MyBuyedProducts.objects.values('producto_comprado_id').filter(usuario_comprador=request.user.id)
    #print(myprod.usuario_comprador.id )
    #print(id_prod)
    products = Product.objects.all().filter( id__in =id_prod )
    
    #print()
    #print(products)
    #products = MyBuyedProducts.objects.all()
    #condicional de categoria
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = MyBuyedProducts.filter(category=category)
    if request.method == 'POST':
        print('post en produc list')
    return render(request, 'my_library/product/list.html',
        {'category': category, 'categories': categories, 'my_products': products, 'section': 'product_listLogin'})

def my_product_detail(request, slug, id):
    #print('')
    #print('pre_rating')
    product = get_object_or_404(Product,
                                id = id,
                                slug=slug,)
    #print('postgetobject')
    #print(product)
    
    #categories = Category.objects.all()
    #product= get_object_or_404(Product,id = id,slug=slug,)
    #print(request.method)
    categories = Category.objects.all()
    
    #print(request.method)
    return render(request,
                  'my_library/product/detail.html',
                  {'product': product,'categories': categories,'slug':slug,'id':id}) #calification form

def review_product(request, id,slug):
    #print('se ejecuto submit')
    product = get_object_or_404(Product, id = id )
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ReviewCreateForm(request.POST)
        if form.is_valid():

            Calificacion.objects.create(product = product, user =  request.user , rating = form.cleaned_data['rating'])
            messages.success(request, 'calificacion dada correctamente')
            product.promedio(form.cleaned_data['rating'])
            return render(request,'my_library/product/detail.html',{'product':product,'categories':categories})
        else:
            form = ReviewCreateForm()
    else:
        form = ReviewCreateForm()

            #Calificacion.objects.create(created_by__id = request.user.id,product__id = id)
       
    return render(request,
                  'my_library/product/detail.html',
                  {'product': product,'categories': categories,'form':form, 'slug': slug, 'id': id})





"""import mimetypes

def download_file(request):
    pa_prod = MyBuyedProducts(request)
    id_prod = MyBuyedProducts.objects.values('producto_comprado_id').filter(usuario_comprador=request.user.id)
    fl_path = Product.objects.all().filter(id_in = id_prod)"""

