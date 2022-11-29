from django.urls import path
from . import views
app_name = 'cart'

#rutas de las funciones indicadas en cart.py para la pagina web
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
