import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = "Bloggo Doggo"
    link = reverse_lazy("blog:post_list")
    description = "New doggo posts every other time!"

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item: Post):
        return item.title

    def item_description(self, item: Post) -> str:
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item: Post):
        return item.publish
