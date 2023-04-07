from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import Category, Post, Comment, CategoryTag

# Register your models here.


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = [
        "status",
        "created",
        "publish",
        "author",
        "categories",
        "tags",
    ]
    search_fields = ["title", "body", "categories", "tags"]
    prepopulated_fields = {"slug": ("title",)}
    # raw_id_fields = ['author']
    ordering = ["status", "publish"]
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


class FeaturedPost(Post):
    class Meta:
        proxy = True


@admin.register(FeaturedPost)
class FeaturedPostAdmin(PostAdmin):
    # list_display = ["title", "categories", "status", "publish", "status"]
    ordering = ["categories", "status", "featured_order", "publish"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_featured=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "updated", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]


@admin.register(CategoryTag)
class CategoryTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ("name",)
