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
    order_by = forms.ChoiceField(
        choices=(("relevance", "Relevance"), ("date", "Date")),
        initial="relevance",
        required=False,
        label="Sort by",
    )
    is_ascending = forms.BooleanField(required=False, initial=False, label="Ascending")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "blog:post_search"
        self.helper.form_method = "get"

        self.helper.layout = Layout(
            Field("query", title=""),
            HTML(
                """<div id="adv-search-expand" class="block has-text-weight-medium">
                Advanced Search Options <span class="icon"><i class="fa-solid fa-angle-up"></i></span>
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
            Div(
                Field(
                    "order_by",
                    wrapper_class="is-horizontal is-flex is-align-items-flex-end is-flex-direction-row",
                ),
                Field(
                    "is_ascending",
                    type="hidden",
                    id="search-is-ascending",
                ),
                HTML(
                    f"""
                    <span id="search-is-ascending-indicator" class="icon is-medium is-clickable has-text-primary">
                        <i class="fa-solid fa-lg fa-arrow-{"up" if self.data.get("is_ascending") == "true" else"down"}-long"></i>
                    </span>
                    """
                ),
                css_class="is-flex search-order-by is-align-items-baseline",
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
