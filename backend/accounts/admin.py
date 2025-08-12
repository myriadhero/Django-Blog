from core.widgets import CroppingImageWidget
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm

from .models import UserProfile

User = get_user_model()


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        widgets = {"avatar": CroppingImageWidget}

    def __init__(self, *args, **kwargs):
        self.base_fields["avatar"].widget.aspect_ratio = 1
        self.base_fields["avatar"].widget.is_curcular = True
        super().__init__(*args, **kwargs)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    form = UserProfileForm


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inlines(self, request, obj=None):
        inlines = super().get_inlines(request, obj)
        if obj is None:
            return [inl for inl in inlines if inl not in self.inlines]
        return inlines


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
