from django import template

register = template.Library()

@register.filter
def dict_get(obj, key):
    return getattr(obj, key, '')
