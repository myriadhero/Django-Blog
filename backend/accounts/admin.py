from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from imagefield.fields import ImageField

from .models import UserProfile
from .widgets import CroppingImageWidget

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    formfield_overrides = {
        ImageField: {"widget": CroppingImageWidget},
    }


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inlines(self, request, obj=None):
        inlines = super().get_inlines(request, obj)
        if obj is None:
            return [inl for inl in inlines if inl not in self.inlines]
        return inlines


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
