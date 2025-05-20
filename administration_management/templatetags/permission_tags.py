from django import template
from administration_management.models import AppPermission

register = template.Library()

@register.filter
def filter(permissions, app_name):
    return permissions.filter(app_name=app_name).first()

