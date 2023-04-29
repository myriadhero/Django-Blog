from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

from .models import Category, CategoryTag, Comment, FeaturedPost, Post


# Register your models here.
class FeaturedPostInline(admin.TabularInline):
    model = FeaturedPost
    extra = 1
    readonly_fields = ("post_status",)

    def post_status(self, instance):
        return instance.post.status

    post_status.short_description = "Post Status"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "slug",
        "name",
        "show_on_front_page",
        "show_in_menu",
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status", "get_categories"]
    list_filter = [
        "status",
        "created",
        "publish",
        "author",
        "categories",
        "tags",
    ]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["status", "publish"]
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}

    def get_categories(self, obj: CategoryTag):
        return ", ".join(cat.name for cat in obj.categories.all())

    get_categories.short_description = "Categories"

    def view_on_site(self, obj: Post):
        if obj.status == Post.Status.PUBLISHED:
            return obj.get_absolute_url()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "updated", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]


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


@admin.register(CategoryTag)
class CategoryTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "get_categories"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    list_filter = ["categories", TagsWithNoPostsFilter]
    readonly_fields = ["get_tagged_posts"]

    def get_categories(self, obj: CategoryTag):
        return ", ".join(cat.name for cat in obj.categories.all())

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
