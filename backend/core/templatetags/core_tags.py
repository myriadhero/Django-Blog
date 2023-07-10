from core.models import SiteIdentity, SocialMedia, SubscriptionOptions
from django import template

register = template.Library()


@register.simple_tag
def get_site_identity():
    return SiteIdentity.objects.get_instance()


@register.simple_tag
def get_subscription_options():
    return SubscriptionOptions.objects.get_instance()


@register.simple_tag
def get_social_media_links():
    return SocialMedia.objects.get_instance()

