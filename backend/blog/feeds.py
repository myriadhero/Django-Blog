from core.models import AboutPage, SiteIdentity
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    title = SiteIdentity.title
    link = reverse_lazy("blog:post_list")
    description = AboutPage.content

    def items(self):
        return Post.published.all()[:15]

    def item_title(self, item: Post):
        return item.title

    def item_description(self, item: Post) -> str:
        return truncatewords_html(item.body, 50)

    def item_pubdate(self, item: Post):
        return item.publish
