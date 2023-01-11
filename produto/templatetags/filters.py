from django.template import Library
from helpers import helpers

register = Library()

#registra o filtro para poder ser utilizado no template
@register.filter
def formata_preco(val):
    return helpers.formata_preco(val)

@register.filter()
def cart_total_items(cart):
    return helpers.cart_total_items(cart)

@register.filter()
def cart_total_value(cart):
    return helpers.cart_total_value(cart)