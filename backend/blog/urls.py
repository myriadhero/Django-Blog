from django.urls import path
from .feeds import LatestPostsFeed
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.FrontPageView.as_view(), name="front_page"),
    path("all/", views.PostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("tag/<slug:tag_slug>/", views.TagPostListView.as_view(), name="posts_by_tag"),
    path(
        "category/<slug:category_slug>/",
        views.CategoryDetailView.as_view(),
        name="category",
    ),
    path("post/<slug:post_slug>/share/", views.post_share, name="post_share"),
    path("post/<slug:post_slug>/comment/", views.post_comment, name="post_comment"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", views.post_search, name="post_search"),
    path("htmx/post_list/", views.PostListHTMXView.as_view(), name="htmx_post_list"),
]
