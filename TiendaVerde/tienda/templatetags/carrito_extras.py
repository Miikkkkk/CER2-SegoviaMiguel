from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def carrito_total(items):
    total = sum(item.cantidad * item.producto.precio for item in items)
    return total


