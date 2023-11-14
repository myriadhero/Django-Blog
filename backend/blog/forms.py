from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms

from .models import Category, CategoryTag, Post, Subcategory


class AdvancedSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        strip=True,
        max_length=100,
        label=False,
    )
    categories = forms.ModelMultipleChoiceField(
        Category.objects.all(), required=False, to_field_name="slug"
    )
    subcategories = forms.ModelMultipleChoiceField(
        Subcategory.objects.all(), required=False, to_field_name="slug"
    )
    tags = forms.ModelMultipleChoiceField(
        CategoryTag.non_empty.all(), required=False, to_field_name="slug"
    )
    before = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    after = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "blog:post_search"
        self.helper.form_method = "get"
        self.helper.layout = Layout(
            Field("query", title=""),
            HTML(
                """<div id="adv-search-expand" class="block">
                Advanced search options <span class="icon"><i class="fa-solid fa-angle-up"></i></span>
                </div>"""
            ),
            Div(
                "categories",
                "subcategories",
                "tags",
                "before",
                "after",
                css_class="collapsed block",
                css_id="adv-search",
            ),
            Submit("submit", "Search", css_class="button is-primary block"),
        )

        if Post.published.exists():
            min_date = Post.published.order_by("publish").first().publish.date()
            max_date = Post.published.first().publish.date()
            self.fields["before"].widget.attrs["min"] = min_date
            self.fields["before"].widget.attrs["max"] = max_date
            self.fields["after"].widget.attrs["min"] = min_date
            self.fields["after"].widget.attrs["max"] = max_date
