from django import template
register = template.Library()

@register.filter(name='isInCart')
def isInCart(product, cart):
    keys = cart.keys()
    for id in keys:
        try:
            # Attempt to convert id to an integer
            id_as_int = int(id)
            if id_as_int == product.id:
                return True
        except ValueError:
            # Handle the case where id is not a valid integer
            if id.lower() == 'null':
                continue  # Skip 'null' values
    return False


@register.filter(name='cartCount')
def cartCount(product,cart ):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0
    
@register.filter(name='cartPrice')
def cartPrice(product,cart ):
    return product.Price  * cartCount(product,cart)

@register.filter(name='cartTotal')
def totalPrice(products,cart):
    sum = 0 
    for p in products:
        sum+=cartPrice(p,cart)
        
    return sum
    
@register.filter(name='currency')
def currency(num):        
    return "₹"+str(num)