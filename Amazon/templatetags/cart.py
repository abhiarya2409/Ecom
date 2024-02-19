from django import template

register = template.Library()


@register.filter(name="isexistincart")
def isexistincart(product,cart):
    print(cart)
    key= cart.keys()
    
    for i in key:
        if int(i) == product.id:
            return True
    return False


@register.filter(name="cartquantity")
def cartquantity(product,cart):
    # print(cart)
    key= cart.keys()
    
    for i in key:
        if int(i) == product.id:
            return cart.get(i)
    return False


@register.filter(name="total_price")
def total_price(product,cart):
    keys=cart.keys()
    for i in keys:
        return product.product_price * cartquantity(product,cart)
    
    
@register.filter(name="payable_price")
def payable_price(product,cart):
    s=0
    for i in product:
        s=s + total_price(i,cart)
    return s

@register.filter(name="order_price")
def order_price(price,quantity):
   return price*quantity