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
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "min": Post.published.order_by("publish").first().publish.date(),
                "max": Post.published.first().publish.date(),
            }
        ),
    )
    after = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "min": Post.published.order_by("publish").first().publish.date(),
                "max": Post.published.first().publish.date(),
            }
        ),
    )


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["name", "email", "text"]


# class EmailPostForm(forms.Form):
#     name = forms.CharField(max_length=25)
#     email = forms.EmailField()
#     to = forms.EmailField()
#     comments = forms.CharField(required=False, widget=forms.Textarea)
