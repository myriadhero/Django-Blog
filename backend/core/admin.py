from django.contrib import admin
from .models import AboutPage, SiteIdentity, SubscriptionOptions


# Register your models here.
class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return self.model.objects.count() == 0

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        return super().change_view(request, object_id, form_url, extra_context)


class SiteIdentityAdmin(SingletonModelAdmin):
    pass


class AboutPageAdmin(SingletonModelAdmin):
    pass


class SubscriptionOptionsAdmin(SingletonModelAdmin):
    pass


admin.site.register(SiteIdentity, SiteIdentityAdmin)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(SubscriptionOptions, SubscriptionOptionsAdmin)
