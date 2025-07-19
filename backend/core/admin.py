from django.contrib import admin

from .models import (
    AboutPage,
    GoogleAdsense,
    SiteIdentity,
    SocialMedia,
    SubscriptionOptions,
    TermsPage,
)


# Register your models here.
class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return self.model.objects.count() == 0

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        return super().change_view(request, object_id, form_url, extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteIdentity)
class SiteIdentityAdmin(SingletonModelAdmin):
    pass


@admin.register(AboutPage)
class AboutPageAdmin(SingletonModelAdmin):
    pass


@admin.register(TermsPage)
class TermsPageAdmin(SingletonModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["title", "content"],
                "description": "Note: To display the Terms of Service page on the site, it must be enabled in the Site Identity settings.",
            },
        ),
    ]


@admin.register(SubscriptionOptions)
class SubscriptionOptionsAdmin(SingletonModelAdmin):
    pass


@admin.register(SocialMedia)
class SocialMediaLinksAdmin(SingletonModelAdmin):
    pass


@admin.register(GoogleAdsense)
class GoogleAdsenseAdmin(SingletonModelAdmin):
    pass
