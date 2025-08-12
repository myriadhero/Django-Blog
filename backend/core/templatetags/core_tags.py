from django import template

from core.models import (
    GoogleAdsense,
    PrivacyPage,
    SiteIdentity,
    SocialMedia,
    SubscriptionOptions,
    TermsPage,
)

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


@register.simple_tag(takes_context=True)
def get_default_meta(context):
    return SiteIdentity.objects.get_instance().as_meta(context["request"])


@register.simple_tag()
def get_adsense_settings():
    return GoogleAdsense.objects.get_instance()


@register.simple_tag()
def get_terms_page():
    return TermsPage.objects.get_instance()


@register.simple_tag()
def get_privacy_page():
    return PrivacyPage.objects.get_instance()
