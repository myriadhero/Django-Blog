from django.forms import ClearableFileInput
from django.template.loader import render_to_string


class CroppingImageWidget(ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.aspect_ratio = attrs.get("aspect_ratio", 0) if attrs else 0
        self.is_curcular = attrs.get("is_curcular", False) if attrs else False

    class Media:
        js = ("js/libraries/cropperv1/cropper.min.js", "js/widgets/cropper_widget.js")
        css = {"all": ("js/libraries/cropperv1/cropper.min.css", "css/widgets/cropper_widget.css")}

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        extra_template = render_to_string(
            "widgets/cropper_widget.html",
            {"name": name, "value": value, "aspect_ratio": self.aspect_ratio, "is_curcular": self.is_curcular},
        )
        output += extra_template
        return output
