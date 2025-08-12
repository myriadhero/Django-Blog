import re

from django import template
from django.template.defaultfilters import truncatewords_html
from lxml import html

from ..models import NavItem, Post
from ..views import RECOMMENDED_POSTS_NUM

TWEET_RE = re.compile(
    r'<blockquote class=["\']twitter-tweet["\'].*?</blockquote>',
    re.DOTALL,
)


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=RECOMMENDED_POSTS_NUM):
    latest_posts = Post.published.all()[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_latest_posts(count=RECOMMENDED_POSTS_NUM):
    return Post.published.exclude(preview_image__isnull=True).exclude(preview_image="")[:count]


# @register.simple_tag
# def get_most_commented_posts(count=RECOMMENDED_POSTS_NUM):
#     return Post.published.annotate(total_comments=Count("comments"))[:count]


@register.simple_tag
def get_nav_items():
    return NavItem.objects.select_related("primary_category").prefetch_related("sub_items__subcategory").all()


@register.simple_tag(takes_context=True)
def get_page_url(context, page):
    query = context["request"].GET.copy()
    query["page"] = page
    return f"?{query.urlencode()}"


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
    match = TWEET_RE.search(body)
    if match:
        return match.group(0)

    return truncatewords_html(body, word_num)
