from django.forms import ClearableFileInput
from django.template.loader import render_to_string


class CroppingImageWidget(ClearableFileInput):
    class Media:
        js = ("js/libraries/cropperv1/cropper.min.js", "js/admin/cropper_widget.js")
        css = {"all": ("js/libraries/cropperv1/cropper.min.css", "css/admin/cropper_widget.css")}

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        extra_template = render_to_string(
            "admin/accounts/user_profile/cropper_widget.html",
            {"name": name, "value": value},
        )
        output += extra_template
        return output
