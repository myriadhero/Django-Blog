from django import template
from core.models import SiteIdentity, SubscriptionOptions

register = template.Library()


@register.simple_tag
def get_site_identity():
    return SiteIdentity.objects.get_instance()


@register.simple_tag
def get_subscription_options():
    return SubscriptionOptions.objects.get_instance()
