from django.forms import ClearableFileInput
from django.template.loader import render_to_string


class CroppingImageWidget(ClearableFileInput):
    def __init__(self, aspect_ratio=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aspect_ratio = aspect_ratio

    class Media:
        js = ("js/libraries/cropperv1/cropper.min.js", "js/admin/cropper_widget.js")
        css = {"all": ("js/libraries/cropperv1/cropper.min.css", "css/admin/cropper_widget.css")}

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        extra_template = render_to_string(
            "admin/accounts/user_profile/cropper_widget.html",
            {"name": name, "value": value, "aspect_ratio": self.aspect_ratio},
        )
        output += extra_template
        return output
