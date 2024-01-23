from core.models import SiteIdentity
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .forms import AdvancedSearchForm
from .models import Category, CategoryTag, FeaturedPost, Post, Subcategory

POSTS_PER_PAGE = 20
RECOMMENDED_POSTS_NUM = 5


# Create your views here.
class PostListView(ListView):
    queryset = (
        Post.published.select_related("author")
        .prefetch_related("categories", "tags", "subcategories")
        .distinct()
    )
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = SiteIdentity.objects.get_instance().as_meta(self.request)
        meta.title = f"{meta.title} - All Posts"
        context["meta"] = meta
        return context

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["blog/post/includes/post_list.html"]
        return super().get_template_names()


class TagPostListView(PostListView):
    def get_queryset(self):
        tag = get_object_or_404(CategoryTag, slug=self.kwargs.get("tag_slug"))
        return super().get_queryset().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(
            CategoryTag, slug=self.kwargs.get("tag_slug"),
        )
        context["meta"] = context["tag"].as_meta(self.request)
        return context


class SubcategoryPostListView(PostListView):
    def get_queryset(self):
        qs = super().get_queryset()

        if cat_slug := self.kwargs.get("category_slug"):
            category = get_object_or_404(Category, slug=cat_slug)
            qs = qs.filter(categories=category)

        subcategory = get_object_or_404(
            Subcategory, slug=self.kwargs.get("subcategory_slug"),
        )

        if (tag_slug := self.request.GET.get("tag")) and (
            tag := CategoryTag.objects.filter(slug=tag_slug).first()
        ):
            qs = qs.filter(tags=tag)

        return qs.filter(subcategories=subcategory)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if cat_slug := self.kwargs.get("category_slug"):
            category = get_object_or_404(Category, slug=cat_slug)
            context["category"] = category

        if (tag_slug := self.request.GET.get("tag")) and (
            tag := CategoryTag.objects.filter(slug=tag_slug).first()
        ):
            context["selected_tag"] = tag

        subcat = get_object_or_404(
            Subcategory, slug=self.kwargs.get("subcategory_slug"),
        )
        context["subcategory"] = subcat
        context["meta"] = subcat.as_meta(self.request)
        context["tags"] = context["subcategory"].get_tags_that_have_at_least_one_post()

        return context

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return ["blog/post/includes/post_list.html"]
        return ["blog/categories/subcategory_post_list.html"]


class CategoryDetailView(ListView):
    paginate_by = POSTS_PER_PAGE
    context_object_name = "posts"

    def get_queryset(self):
        category = self.get_category()
        if category.is_tag_list:
            return Post.objects.none()

        queryset = (
            Post.published.filter(categories=category)
            .select_related("author")
            .prefetch_related("categories", "tags")
        )
        tag_slug = self.request.GET.get("tag", None)
        if tag_slug:
            # TODO: this probably should NOT return 404, but ignore wrong tag instead
            tag = get_object_or_404(CategoryTag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        return queryset

    def get_template_names(self):
        category = self.get_category()
        if category.is_tag_list:
            return ["blog/categories/tag_list.html"]
        if self.request.headers.get("HX-Request"):
            return ["blog/post/includes/post_list.html"]
        return ["blog/categories/category_post_list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context["category"] = category
        context["meta"] = category.as_meta(self.request)
        context["tags"] = (category.categorytag_set.all()
                           if category.is_tag_list
                           else category.get_tags_that_have_at_least_one_post())

        tag_slug = self.request.GET.get("tag", None)
        if tag_slug:
            # TODO: this probably should NOT return 404, but ignore wrong tag instead
            tag = get_object_or_404(CategoryTag, slug=tag_slug)
            context["selected_tag"] = tag

        return context

    def get_category(self) -> Category:
        return get_object_or_404(Category, slug=self.kwargs["category_slug"])


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["similar_posts"] = post.get_similar_posts(RECOMMENDED_POSTS_NUM)
        context["meta"] = post.as_meta(self.request)
        return context


class FrontPageView(ListView):
    context_object_name = "categories"
    template_name = "blog/front_page/front_page.html"

    def get_queryset(self):
        featured_posts_with_posts = FeaturedPost.published.select_related("post").all()
        prefetch_featured_posts = Prefetch(
            "featured_posts",
            queryset=featured_posts_with_posts,
            to_attr="published_featured_posts",
        )
        categories = Category.on_front_page.prefetch_related(
            prefetch_featured_posts,
        ).all()
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = SiteIdentity.objects.get_instance().as_meta(self.request)
        return context


class PostSearchListView(PostListView):
    template_name = "blog/post/search.html"
    form_class = AdvancedSearchForm

    def get_queryset(self):
        qs = super().get_queryset()
        form = self.form_class(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]
            categories = form.cleaned_data["categories"]
            subcategories = form.cleaned_data["subcategories"]
            tags = form.cleaned_data["tags"]
            before = form.cleaned_data["before"]
            after = form.cleaned_data["after"]
            order_by = form.cleaned_data["order_by"]
            is_ascending = "" if form.cleaned_data["is_ascending"] else "-"

            if not any((query, categories, subcategories, tags, before, after)):
                return qs.none()

            if query:
                search_vector = SearchVector("title", "body")
                search_query = SearchQuery(query)
                qs = qs.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query),
                ).filter(search=search_query)

            if categories:
                qs = qs.filter(categories__in=categories)

            if subcategories:
                qs = qs.filter(subcategories__in=subcategories)

            if tags:
                qs = qs.filter(tags__in=tags)

            if before:
                qs = qs.filter(publish__lt=before)

            if after:
                qs = qs.filter(publish__gt=after)

            qs = qs.order_by(
                f"{is_ascending}{'publish' if order_by=='date' else 'rank'}",
            )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.GET)
        site_identity = SiteIdentity.objects.get_instance()
        meta = site_identity.as_meta(self.request)
        meta.title = f"Search {site_identity.title}"
        context["meta"] = meta
        return context
