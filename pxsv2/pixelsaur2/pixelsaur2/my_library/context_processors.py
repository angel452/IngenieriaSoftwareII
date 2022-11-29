from .models import MyBuyedProducts
def my_products(request):
    return {'MyBuyedProducts': MyBuyedProducts(request)}