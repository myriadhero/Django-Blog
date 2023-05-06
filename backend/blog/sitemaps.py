from django.contrib.sitemaps import Sitemap

from .models import Category, Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj: Post):
        return obj.updated


class CategorySitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj: Category):
        return Post.published.filter(categories=obj).first().updated
