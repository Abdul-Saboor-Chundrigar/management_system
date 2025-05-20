from django import template

register = template.Library()

@register.filter
def dict_key(obj, key):
    return getattr(obj, key, None)
