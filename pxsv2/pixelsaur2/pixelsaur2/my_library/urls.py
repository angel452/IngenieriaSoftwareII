from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = 'my_library'

urlpatterns = [
    path('',views.my_product_list, name='my_product_list'),
    path('<slug:category_slug>/',views.my_product_list, name='my_product_list_by_category'),
    path('<int:id>/<slug:slug>',views.my_product_detail, name='my_product_detail'),
    path('review/<int:id>/<slug:slug>' ,views.review_product, name='review_product'),
]