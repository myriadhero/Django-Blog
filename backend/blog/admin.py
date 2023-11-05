from itertools import chain
from typing import Any

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin, messages
from django.contrib.admin.utils import model_ngettext
from django.core.validators import validate_slug
from django.db import models
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _
from django_select2 import forms as s2forms

from .models import (
    Category,
    CategoryTag,
    DropdownNavItem,
    FeaturedPost,
    NavItem,
    Post,
    Subcategory,
)


# Register your models here.
class FeaturedPostInline(admin.TabularInline):
    model = FeaturedPost
    extra = 1
    readonly_fields = ("post_status",)

    def post_status(self, instance):
        return instance.post.status

    post_status.short_description = "Post Status"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "post":
            category_id = request.resolver_match.kwargs.get("object_id")
            if category_id:
                category = Category.objects.get(pk=category_id)
                kwargs["queryset"] = Post.objects.filter(categories=category)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DropdownNavItemInline(admin.TabularInline):
    model = DropdownNavItem
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "show_on_front_page",
        "order",
        "is_tag_list",
    ]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [FeaturedPostInline]
    readonly_fields = ["get_posts_in_category"]

    def get_posts_in_category(self, obj: Category):
        posts = obj.post_set.all()[:20]
        html_links = format_html_join(
            "\n",
            '<div><a href="{}">{}</a></div>',
            (
                (reverse("admin:blog_post_change", args=[post.pk]), post.title)
                for post in posts
            ),
        )
        html_see_all = format_html(
            '<div><a href="{}">Show all</a></div>',
            reverse("admin:blog_post_changelist") + f"?categories__id__exact={obj.pk}",
        )
        return format_html("{}<br>{}", html_links, html_see_all)

    get_posts_in_category.short_description = "Posts in category"


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "get_categories",
    ]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["get_posts_in_category"]
    ordering = ["name"]

    def get_posts_in_category(self, obj: Subcategory):
        posts = obj.post_set.all()[:20]
        html_links = format_html_join(
            "\n",
            '<div><a href="{}">{}</a></div>',
            (
                (reverse("admin:blog_post_change", args=[post.pk]), post.title)
                for post in posts
            ),
        )
        html_see_all = format_html(
            '<div><a href="{}">Show all</a></div>',
            reverse("admin:blog_post_changelist")
            + f"?subcategories__id__exact={obj.pk}",
        )
        return format_html("{}<br>{}", html_links, html_see_all)

    get_posts_in_category.short_description = "Posts in category"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related("categories")

    def get_categories(self, obj: CategoryTag):
        return ", ".join(cat.name for cat in obj.categories.all())

    get_categories.short_description = "Categories"


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "order", "is_dropdown"]
    inlines = [DropdownNavItemInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).select_related("primary_category")


class TagsAutoMultiSelectWidget(s2forms.ModelSelect2TagWidget):
    search_fields = [
        "name__icontains",
    ]

    queryset = CategoryTag.objects.all()

    def value_from_datadict(self, data, files, name):
        """Create objects for given non-pimary-key values. Return list of all primary keys."""
        values = set(super().value_from_datadict(data, files, name))

        pks = self.queryset.filter(
            **{"pk__in": list(filter(lambda x: x.isdigit(), values))}
        ).values_list("pk", flat=True)

        pks = set(map(str, pks))

        cleaned_values = list(pks)
        for val in values - pks:
            if not (new_tag := CategoryTag.objects.filter(name=val).first()):
                new_tag = CategoryTag(name=val)
                new_tag.save()
            cleaned_values.append(str(new_tag.pk))

        return cleaned_values


class PostAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=CategoryTag.objects.all(),
        required=False,
        widget=TagsAutoMultiSelectWidget(
            attrs={"data-token-separators": [","], "data-tags": "true"}
        ),
    )

    class Meta:
        model = Post
        exclude = ["tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tags"].initial = self.instance.tags.all()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ["title", "slug", "author", "publish", "status", "get_categories"]
    list_filter = [
        "status",
        "created",
        "publish",
        "author",
        "categories",
        "subcategories",
        "tags",
    ]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}
    autocomplete_fields = ["tags"]
    ordering = ["status", "-publish"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Post]:
        qs = (
            super()
            .get_queryset(request)
            .select_related("author")
            .prefetch_related(
                "categories",
                "subcategories",
            )
        )
        return qs

    def get_categories(self, obj: Post):
        return ", ".join(
            cat.name for cat in chain(obj.categories.all(), obj.subcategories.all())
        )

    get_categories.short_description = "Categories"

    def view_on_site(self, obj: Post):
        if obj.status == Post.Status.PUBLISHED:
            return obj.get_absolute_url()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.tags.set(form.cleaned_data["tags"])


class TagsWithNoPostsFilter(admin.SimpleListFilter):
    title = _("other filters")

    parameter_name = "no-posts"

    def lookups(self, request, model_admin):
        return [("", "Tags without any posts")]

    def queryset(self, request, queryset):
        if self.value() == "":
            return queryset.annotate(
                ntag=Count("blog_taggedwithcategorytags_tags")
            ).filter(ntag=0)


class CategoryTagAdminForm(forms.ModelForm):
    class Meta:
        model = CategoryTag
        fields = "__all__"

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        validate_slug(slug)
        return slug


@admin.register(CategoryTag)
class CategoryTagAdmin(admin.ModelAdmin):
    form = CategoryTagAdminForm
    list_display = ["name", "slug", "description", "get_categories"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    list_filter = [
        "categories",
        TagsWithNoPostsFilter,
        ("description", admin.EmptyFieldListFilter),
        ("preview_image", admin.EmptyFieldListFilter),
    ]
    readonly_fields = ["get_tagged_posts"]
    actions = [
        "remove_tags_from_posts",
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = (
            super()
            .get_queryset(request)
            .prefetch_related("categories", "subcategories")
        )
        return qs

    def get_categories(self, obj: CategoryTag):
        return ", ".join(
            cat.name for cat in chain(obj.categories.all(), obj.subcategories.all())
        )

    get_categories.short_description = "Categories"

    def get_tagged_posts(self, obj: CategoryTag):
        posts = obj.get_tagged_posts()[:20]
        html_links = format_html_join(
            "\n",
            '<div><a href="{}">{}</a></div>',
            (
                (reverse("admin:blog_post_change", args=[post.pk]), post.title)
                for post in posts
            ),
        )
        html_see_all = format_html(
            '<div><a href="{}">Show all</a></div>',
            reverse("admin:blog_post_changelist") + f"?tags__id__exact={obj.pk}",
        )
        return format_html("{}<br>{}", html_links, html_see_all)

    get_tagged_posts.short_description = "Tagged posts"

    @admin.action(description="Remove selected items as tags from all posts")
    def remove_tags_from_posts(self, request, queryset):
        tags_and_posts = {
            tag: list(tag.get_tagged_posts().all())
            for tag in queryset
        }

        if not any(tags_and_posts.values()):
            self.message_user(
                request,
                "No posts found with selected tags.",
                messages.INFO,
            )
            return None

        # if POST, action the removal
        if request.POST.get("post"):
            all_tags = tags_and_posts.keys()
            for post in set(chain(*tags_and_posts.values())):
                post.tags.remove(*all_tags)

            self.message_user(
                request,
                "Selected tags removed from all posts.",
                messages.SUCCESS,
            )
            return None

        context = {
            **self.admin_site.each_context(request),
            "title": _("Are you sure?"),
            "subtitle": None,
            "objects_name": model_ngettext(queryset),
            "queryset": queryset,
            "affected_posts_by_tag": tags_and_posts,
            "media": self.media,
            "opts": self.model._meta,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        }

        request.current_app = self.admin_site.name

        # Display the confirmation page
        return TemplateResponse(
            request,
            "admin/blog/categorytag/remove_tags_from_posts.html",
            context,
        )
