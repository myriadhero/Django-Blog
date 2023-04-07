from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
from ..models import Post, Category

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.all()[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments"))[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown(text))


@register.simple_tag
def get_menu_categories():
    return Category.in_menu.all()


@register.simple_tag
def paginated_htmx_link(url, page, category=None, tag=None):
    url = f"{url}?page={page}"
    if category:
        url += f"&category={category.slug}"
    if tag:
        url += f"&tag={tag.slug}"
    return url
