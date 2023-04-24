from django import template
from core.models import SiteIdentity

register = template.Library()

@register.simple_tag
def get_site_identity():
    return SiteIdentity.objects.get_instance()
