from decimal import Decimal
from django.conf import settings
from pixelsaurapp.models import Product
from coupons.models import Coupon

#metodo carro donde definira las funciones de carrito de compras
class Cart(object):
    """
    EL init  toma la session de la web para guardar los datos, 
    tambien toma la session para aplica al cupon.
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Agrega elementos para una futura tabla compras
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
            'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    def save(self):
        # guarda la sesion true para asegurar que se guarde 
        self.session.modified = True
    def remove(self, product):
        """
        Funcion para remover el producto del carro
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterar sobre los artículos en el carrito y obtener los productos.
        de la base de datos
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Cuente todos los artículos en el carrito.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        # tenemos el precio total
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # removemos el carro de la session
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    @property
    def coupon(self):
        #FUncion booleana para consulta de carrito
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        #aplicar el descuento a partir de la cantidad indicada
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
            * self.get_total_price()
        return Decimal(0)
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()