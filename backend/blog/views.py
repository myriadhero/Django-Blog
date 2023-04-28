from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count, Prefetch
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post, Category, CategoryTag, FeaturedPost
from .forms import EmailPostForm, CommentForm, SearchForm

POSTS_PER_PAGE = 3
RECOMMENDED_POSTS_NUM = 5


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE
    template_name = "blog/post/list.html"


class TagPostListView(PostListView):
    def get_queryset(self):
        tag = get_object_or_404(CategoryTag, slug=self.kwargs.get("tag_slug"))
        return Post.published.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(
            CategoryTag, slug=self.kwargs.get("tag_slug")
        )
        return context


class PostListHTMXView(PostListView):
    template_name = "blog/post/includes/post_list.html"

    def get_queryset(self):
        queryset = Post.published

        category_slug = self.request.GET.get("category", None)
        tag_slug = self.request.GET.get("tag", None)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=category)

        if tag_slug:
            tag = get_object_or_404(CategoryTag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.request.GET.get("category", None)
        tag_slug = self.request.GET.get("tag", None)

        if category_slug:
            context["category"] = get_object_or_404(Category, slug=category_slug)

        if tag_slug:
            context["selected_tag"] = get_object_or_404(CategoryTag, slug=tag_slug)

        return context


class CategoryDetailView(ListView):
    paginate_by = POSTS_PER_PAGE
    context_object_name = "posts"

    def get_queryset(self):
        category = self.get_category()
        if category.is_tag_list:
            return Post.objects.none()

        queryset = Post.published.filter(categories=category)
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


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["form"] = CommentForm()
        context["comments"] = post.comments.filter(active=True)
        context["similar_posts"] = self.get_similar_posts()
        return context

    def get_queryset(self):
        return Post.published.filter(slug=self.kwargs["slug"])

    def get_similar_posts(self):
        post = self.get_object()
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags"
        )[:RECOMMENDED_POSTS_NUM]

        return similar_posts


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


def post_search(request):
    # TODO: convert to class based view and implement pagination
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", "body")
            search_query = SearchQuery(query)

            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(search=search_query)
                .order_by("-rank")
            )
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post.published, slug=slug)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request, post_slug):
    post: Post = get_object_or_404(Post.published, slug=post_slug)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'My doggo {cd["name"]} recommends you {post.title}'
            message = (
                f"Hello dis doggo here\n\n{cd['comments']}\n\nread more at {post_url}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=cd["email"],
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"form": form, "sent": sent, "post": post}
    )


@require_POST
def post_comment(request, post_slug):
    post = get_object_or_404(Post.published, slug=post_slug)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {
            "post": post,
            "form": form,
            "comment": comment,
        },
    )
