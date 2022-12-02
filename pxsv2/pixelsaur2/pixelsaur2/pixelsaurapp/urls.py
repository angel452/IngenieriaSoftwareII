from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pixelsaurapp'

urlpatterns = [
    path('', views.product_list, name='product_list'), #nombre en el setings
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',  views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/regalo',  views.form_regalo, name='form_regalo'),
    path('busqueda', views.search_view, name='search_view'),
    path('pedir-dinero',views.pedir_dinero, name='pedir_dinero'),
    #path('<int:id>/<slug:slug>/', views.regalo_create, name='regalo_create'),
    #path('<str:slug>/', ItemsByCategoryView.as_view() , name='category-detail'),

    
]