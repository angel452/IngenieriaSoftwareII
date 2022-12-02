from decimal import Decimal
from django.conf import settings
from pixelsaurapp.models import Product
from coupons.models import Coupon
from account.models import Wallet
from django.contrib.auth.models import User


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
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
    
    """
    Agrega elementos para una futura tabla compras
    """
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        code = str(product.id)+str(product.name)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
            'price': str(product.price) , 'code':code}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

        
    # guarda la sesion true para asegurar que se guarde en proximos login
    def save(self):
        self.session.modified = True

    """
    Funcion para remover el producto del carro
    """
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    """
    Iterar sobre los artículos en el carrito y obtener los productos.
    de la base de datos
    """
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)#obtenemos el grupo de productos para copiarlos en iteracion
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    """
    Cuente todos los artículos en el carrito.
    """
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

  
    # tenemos el precio total
    #f code_discount = id+name
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    
    #removemos el carro de la session
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    #FUncion booleana para consulta de carrito, verificar que el cupon corresponda al id del producto
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    # funcion para aplicar el descuento a partir de la cantidad indicada
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
            * self.get_total_price()
        return Decimal(0)


    #funcion para restar el precio del producto despues de comparar el producto con el codigo de descuento    
    def get_specific_discount(self):
        suma = 0
        
        if self.coupon:
            for item in self.cart.values():
                if self.coupon.code == item['code']:
                    suma += Decimal(self.coupon.discount / Decimal(100)) \
                        * item['price']
                else:
                    suma += item['price']
            return suma
        else:
            return self.get_total_price()
                
    #funcion para obtener el precio total del producto despues de aplicar el descuento        
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()


    #funcion extra para verficar restar el precio de billetera
    def cobrar_orden(self):
        if User.Wallet.money > self.get_total_price_after_discount():
            return 'no hay dinero suficiente'
        else:
            User.Wallet.money = User.Wallet.money - self.get_total_price_after_discount()
            return 'correcto'
    
            
        