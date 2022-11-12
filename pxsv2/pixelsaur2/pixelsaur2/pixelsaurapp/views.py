from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

#for Login
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#from .forms import LoginForm

#muestra una lista de productos por categoria
@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    #condicional de categoria
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'pixelsaurapp/product/list.html',
        {'category': category, 'categories': categories, 'products': products, 'section': 'product_listLogin'})

#muestra el detalle del producto cuando se le hace click
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'pixelsaurapp/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})