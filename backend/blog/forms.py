from django import forms

from .models import Category, CategoryTag, Post


class AdvancedSearchForm(forms.Form):
    query = forms.CharField(required=False, strip=True, max_length=200)
    categories = forms.ModelMultipleChoiceField(
        Category.objects.all(), required=False, to_field_name="slug"
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

        if Post.published.exists():
            min_date = Post.published.order_by("publish").first().publish.date()
            max_date = Post.published.first().publish.date()
            self.fields["before"].widget.attrs["min"] = min_date
            self.fields["before"].widget.attrs["max"] = max_date
            self.fields["after"].widget.attrs["min"] = min_date
            self.fields["after"].widget.attrs["max"] = max_date


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["name", "email", "text"]


# class EmailPostForm(forms.Form):
#     name = forms.CharField(max_length=25)
#     email = forms.EmailField()
#     to = forms.EmailField()
#     comments = forms.CharField(required=False, widget=forms.Textarea)
