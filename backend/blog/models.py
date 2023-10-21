from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Count, Exists, OuterRef
from django.db.models.query import QuerySet
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from lxml import html
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase


class FrontPageCatsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(show_on_front_page=True)


class MenuCatsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(show_in_menu=True)


class Category(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    slug = models.SlugField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        unique=True,
        help_text="Please use only letters, numbers, underscores or hyphens; must be unique.",
    )
    description = models.CharField(
        max_length=250, blank=True, help_text="250 characters long"
    )
    group = models.IntegerField(
        default=0,
        help_text="Enter an integer value to define the display group order. Categories are sorted and divided by group first, then order within group.",
    )
    order = models.IntegerField(
        default=0,
        help_text="Enter an integer value to define the display order within a group.",
    )
    preview_image = models.ImageField(upload_to="category_previews/", blank=True)
    show_on_front_page = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=False)
    is_tag_list = models.BooleanField(
        default=False,
        help_text="If enabled, this category will show a list of tags first instead of posts+tag filters.",
    )

    thumbnail = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(200, 200)],
        format="jpeg",
        options={"quality": 60},
    )

    objects = models.Manager()
    on_front_page = FrontPageCatsManager()
    in_menu = MenuCatsManager()

    class Meta:
        ordering = ["group", "order"]
        verbose_name = gettext_lazy("Category")
        verbose_name_plural = gettext_lazy("Categories")

    def get_tags_that_have_at_least_one_post(self):
        if self.is_tag_list:
            tag_relations = TaggedWithCategoryTags.objects.filter(
                tag=OuterRef("pk"),
            )
        else:
            post_content_type = ContentType.objects.get_for_model(Post)
            tag_relations = TaggedWithCategoryTags.objects.filter(
                tag=OuterRef("pk"),
                content_type=post_content_type,
                object_id__in=self.post_set.all(),
            )
        return self.categorytag_set.filter(Exists(tag_relations))

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])


class NonEmptyTagsManager(models.Manager):
    def get_queryset(self):
        tag_relations = TaggedWithCategoryTags.objects.filter(
            tag=OuterRef("pk"),
        )
        return super().get_queryset().filter(Exists(tag_relations))


class SubCatTagsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_sub_category=True)


class CategoryTag(TagBase):
    categories = models.ManyToManyField(Category, blank=True)
    parent_sub_categories = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="children_tags",
        limit_choices_to={"is_sub_category": True},
    )
    is_sub_category = models.BooleanField(
        default=False,
        help_text="⚠ Toggling this will remove this tag from related posts.",
    )
    preview_image = models.ImageField(upload_to="tag_previews/", blank=True)
    description = models.CharField(
        max_length=250, blank=True, help_text="250 characters long"
    )
    thumbnail = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(200, 200)],
        format="jpeg",
        options={"quality": 60},
    )

    objects = models.Manager()
    non_empty = NonEmptyTagsManager()
    sub_categories = SubCatTagsManager()

    class Meta:
        verbose_name = gettext_lazy("Tag with categories")
        verbose_name_plural = gettext_lazy("Tags with categories")
        ordering = ["-is_sub_category", "name"]

    def save(self, *args, **kwargs):
        if self.pk:
            previous_is_sub_category = CategoryTag.objects.get(
                pk=self.pk
            ).is_sub_category

            if not previous_is_sub_category and self.is_sub_category:
                self.parent_sub_categories.clear()
                for post in Post.objects.filter(tags=self):
                    post.tags.remove(self)

            elif previous_is_sub_category and not self.is_sub_category:
                for post in Post.objects.filter(sub_categories=self):
                    post.sub_categories.remove(self)

        return super().save(*args, **kwargs)

    def get_absolute_url(self, **kwargs):
        if not self.is_sub_category:
            return reverse("blog:posts_by_tag", args=[self.slug])
        if current_category := kwargs.get("category_slug"):
            if not self.categories.filter(slug=current_category).exists():
                raise Http404(
                    f"Tag {self.name} does not belong to category {current_category}."
                )
            return reverse(
                "blog:category_sub_category",
                args=[current_category, self.slug],
            )
        return reverse("blog:sub_category", args=[self.slug])

    def get_tagged_posts(self, force_get_category=False, force_get_tagged=False):
        if not force_get_tagged and (self.is_sub_category or force_get_category):
            return self.subcat_posts.all()
        return Post.objects.filter(tags=self)

    def get_all_related_posts(self):
        return Post.objects.filter(models.Q(tags=self) | models.Q(sub_categories=self))


class NavItem(models.Model):
    is_dropdown = models.BooleanField(default=False)
    primary_category = models.OneToOneField(Category, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = gettext_lazy("Navigation Item")
        verbose_name_plural = gettext_lazy("Navigation Items")

    def __str__(self) -> str:
        return f"{self.primary_category.name} Nav"


class DropdownNavItem(models.Model):
    parent_nav_item = models.ForeignKey(
        NavItem, on_delete=models.CASCADE, related_name="sub_items"
    )
    category_tag = models.ForeignKey(
        CategoryTag,
        on_delete=models.CASCADE,
        limit_choices_to={"is_sub_category": True},
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = gettext_lazy("Dropdown Item")
        verbose_name_plural = gettext_lazy("Dropdown Items")

    def __str__(self) -> str:
        return f"{self.parent_nav_item.primary_category.name} Nav Dropdown - {self.category_tag.name} Tag"


class TaggedWithCategoryTags(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CategoryTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_tags",
    )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique=True,
        db_index=True,
        help_text="Please use only letters, numbers, underscores or hyphens; must be unique, auto-insrements if duplicates are found.",
    )
    preview_image = models.ImageField(upload_to="blog_previews/", blank=True)
    prevew_image_credit = models.CharField(
        max_length=500,
        blank=True,
        help_text="Consider adding a credit and a link to the source. 500 characters long.",
    )
    body = RichTextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    categories = models.ManyToManyField(Category)
    sub_categories = models.ManyToManyField(
        CategoryTag,
        blank=True,
        limit_choices_to={"is_sub_category": True},
        related_name="subcat_posts",
    )
    tags = TaggableManager(
        through=TaggedWithCategoryTags,
        verbose_name="Tags with categories",
        help_text="Tags, comma separated",
        related_name="tag_posts",
    )

    objects = models.Manager()
    published = PublishedManager()

    thumbnail = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(210, 210)],
        format="jpeg",
        options={"quality": 60},
    )
    header_image = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(800, 600, upscale=False)],
        format="jpeg",
        options={"quality": 60},
    )
    front_page_image = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(600, 800)],
        format="jpeg",
        options={"quality": 60},
    )

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        self.remove_scripts_from_body()
        self.check_youtube_iframe()
        super().save(*args, **kwargs)

    def get_similar_posts(self, post_num=5):
        post_tags_ids = self.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=self.id
        )

        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags"
        )[:post_num]

        return similar_posts

    def generate_unique_slug(self):
        # TODO: decide whether this should return a slug or set it
        base_slug = self.slug or slugify(self.title)

        if not Post.objects.filter(slug=base_slug).exclude(pk=self.pk).exists():
            self.slug = base_slug
            return base_slug

        main_piece, delim, last_piece = base_slug.rpartition("-")

        if last_piece.isdigit():
            counter = int(last_piece) + 1
            base_slug = main_piece
        else:
            counter = 1

        slug = f"{base_slug}-{counter}"

        while Post.objects.filter(slug=slug).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"

        self.slug = slug
        return slug

    def remove_scripts_from_body(self):
        # TODO: replace with django-bleach, delete script tags from other posts
        root = html.fromstring(self.body)

        for tag in root.xpath("//script"):
            tag.drop_tree()

        self.body = html.tostring(root, encoding="unicode")

    def check_youtube_iframe(self):
        root = html.fromstring(self.body)

        for tag in root.xpath("//iframe"):
            if not tag.attrib.get("src", "").startswith("https://www.youtube.com"):
                tag.drop_tree()

        self.body = html.tostring(root, encoding="unicode")

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __str__(self) -> str:
        return self.title


class FeaturedPostPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post__status=Post.Status.PUBLISHED)


class FeaturedPost(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="featured_posts"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField(
        default=0, help_text="Enter an integer value to define the display order."
    )

    objects = models.Manager()
    published = FeaturedPostPublishedManager()

    class Meta:
        unique_together = ("category", "post")
        ordering = ["order", "-post__publish"]

    def __str__(self):
        return f"{self.category} - {self.post} (Order: {self.order}, Published: {self.post.publish.strftime('%a %d %b %Y, %I:%M%p')})"


# class Comment(models.Model):
#     text = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
#     # parent_comment = models.ForeignKey("self", null=True)
#     active = models.BooleanField(default=True)

#     class Meta:
#         ordering = ["created"]
#         indexes = [
#             models.Index(fields=["created"]),
#         ]

#     def is_updated(self):
#         return self.updated - self.created > timezone.timedelta(minutes=1)

#     def __str__(self) -> str:
#         return f"Comment by {self.name} on {self.post}"
