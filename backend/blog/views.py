from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .forms import AdvancedSearchForm
from .models import Category, CategoryTag, FeaturedPost, Post

POSTS_PER_PAGE = 10
RECOMMENDED_POSTS_NUM = 5


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.select_related("author").prefetch_related(
        "categories", "tags"
    )
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE
    template_name = "blog/post/list.html"


# TODO: fix pagination bug as it seems to not return the correct tagged items
class TagPostListView(PostListView):
    def get_queryset(self):
        tag = get_object_or_404(CategoryTag, slug=self.kwargs.get("tag_slug"))
        return super().get_queryset().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(
            CategoryTag, slug=self.kwargs.get("tag_slug")
        )
        return context


class HTMXPostListView(PostListView):
    template_name = "blog/post/includes/post_list.html"


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
        return ["blog/categories/post_tag_list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context["category"] = category
        context["tags"] = category.get_tags_that_have_at_least_one_post()

        tag_slug = self.request.GET.get("tag", None)
        if tag_slug:
            # TODO: this probably should NOT return 404, but ignore wrong tag instead
            tag = get_object_or_404(CategoryTag, slug=tag_slug)
            context["selected_tag"] = tag

        return context

    def get_category(self) -> Category:
        return get_object_or_404(Category, slug=self.kwargs["category_slug"])


class HTMXCategoryDetailView(CategoryDetailView):
    template_name = "blog/post/includes/post_list.html"

    def get_template_names(self):
        return ["blog/post/includes/post_list.html"]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_posts"] = self.get_object().get_similar_posts(
            RECOMMENDED_POSTS_NUM
        )
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
            prefetch_featured_posts
        ).all()
        return categories


class PostSearchListView(PostListView):
    template_name = "blog/post/search.html"
    form_class = AdvancedSearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]
            categories = form.cleaned_data["categories"]
            tags = form.cleaned_data["tags"]
            before = form.cleaned_data["before"]
            after = form.cleaned_data["after"]

            if not any((query, categories, tags, before, after)):
                return queryset.none()

            if query:
                search_vector = SearchVector("title", "body")
                search_query = SearchQuery(query)
                queryset = (
                    queryset.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query),
                    )
                    .filter(search=search_query)
                    .order_by("-rank")
                )

            if categories:
                for cat in categories:
                    queryset = queryset.filter(categories=cat)

            if tags:
                for tag in tags:
                    queryset = queryset.filter(tags=tag)

            if before:
                queryset = queryset.filter(publish__lt=before)

            if after:
                queryset = queryset.filter(publish__gt=after)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.GET)
        return context


class HTMXPostSearchListView(PostSearchListView):
    template_name = "blog/post/includes/post_list.html"


# def post_share(request, post_slug):
#     post: Post = get_object_or_404(Post.published, slug=post_slug)
#     sent = False
#     if request.method == "POST":
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = f'My doggo {cd["name"]} recommends you {post.title}'
#             message = (
#                 f"Hello dis doggo here\n\n{cd['comments']}\n\nread more at {post_url}"
#             )
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=cd["email"],
#                 recipient_list=[cd["to"]],
#             )
#             sent = True
#     else:
#         form = EmailPostForm()
#     return render(
#         request, "blog/post/share.html", {"form": form, "sent": sent, "post": post}
#     )


# @require_POST
# def post_comment(request, post_slug):
#     post = get_object_or_404(Post.published, slug=post_slug)
#     comment = None

#     form = CommentForm(data=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()

#     return render(
#         request,
#         "blog/post/comment.html",
#         {
#             "post": post,
#             "form": form,
#             "comment": comment,
#         },
#     )
