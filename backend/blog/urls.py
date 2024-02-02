from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", views.FrontPageView.as_view(), name="front_page"),
    path("all/", views.AllPostsView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("tag/<slug:tag_slug>/", views.TagPostListView.as_view(), name="posts_by_tag"),
    path(
        "category/<slug:category_slug>/",
        views.CategoryDetailView.as_view(),
        name="category",
    ),
    path(
        "category/<slug:category_slug>/<slug:subcategory_slug>/",
        views.SubcategoryPostListView.as_view(),
        name="category_subcategory",
    ),
    path(
        "sub-category/<slug:subcategory_slug>/",
        views.SubcategoryPostListView.as_view(),
        name="subcategory",
    ),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", views.PostSearchListView.as_view(), name="post_search"),
]
