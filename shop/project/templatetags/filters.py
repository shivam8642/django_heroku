from django import template
register = template.Library()
@register.simple_tag()
def multiply(quantity, price, *args, **kwargs):
    return quantity * price