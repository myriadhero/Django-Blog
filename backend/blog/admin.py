from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import Category, Post, Comment, CategoryTag, FeaturedPost


# Register your models here.
class FeaturedPostInline(admin.TabularInline):
    model = FeaturedPost
    extra = 1


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "updated", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]


@admin.register(CategoryTag)
class CategoryTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
