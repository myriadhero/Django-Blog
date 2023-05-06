from django import template
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from lxml import html
from markdown import markdown

from ..models import Category, Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.all()[:count]
    return {"latest_posts": latest_posts}


# @register.simple_tag
# def get_most_commented_posts(count=5):
#     return Post.published.annotate(total_comments=Count("comments"))[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown(text))


@register.simple_tag
def get_menu_categories():
    return Category.in_menu.all()


@register.simple_tag(takes_context=True)
def get_page_url(context, page):
    query = context["request"].GET.copy()
    query["page"] = page
    return query.urlencode()


@register.filter(name="html_preview")
def html_preview(value):
    root = html.fromstring(value)
    for tag in root.xpath("//h1|//h2|//h3|//h4"):
        tag.tag = "h5"

    for tag in root.xpath("//img"):
        tag.drop_tag()

    return html.tostring(root, encoding="unicode")


@register.filter(name="tweet_or_truncate")
def tweet_or_truncate(body, word_num=50):
    root = html.fromstring(body)

    for tag in root.xpath("//blockquote"):
        return html.tostring(tag, encoding="unicode")

    return Truncator(body).words(word_num, html=True)
