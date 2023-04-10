from django.contrib.auth.models import User
from django.db import models
from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy, pgettext_lazy
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase
from ckeditor.fields import RichTextField


class FrontPageCatsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(show_on_front_page=True)


class MenuCatsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(show_in_menu=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Please use only letters, numbers, underscores or hyphens; must be unique.",
    )
    description = models.CharField(
        max_length=250, blank=True, help_text="250 characters long"
    )
    order = models.IntegerField(
        default=0, help_text="Enter an integer value to define the display order."
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
        ordering = ["order"]
        verbose_name = gettext_lazy("Category")
        verbose_name_plural = gettext_lazy("Categories")

    def get_featured_posts(self):
        return self.post_set.filter(
            is_featured=True, status=Post.Status.PUBLISHED
        ).order_by("featured_order", "publish")[:5]

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])

    def get_tags_that_have_at_least_one_post(self):
        tag_relations = TaggedWithCategoryTags.objects.filter(tag=OuterRef("pk"))
        return self.categorytag_set.filter(Exists(tag_relations))

    def __str__(self) -> str:
        return self.name


class CategoryTag(TagBase):
    categories = models.ManyToManyField(Category, blank=True)
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

    class Meta:
        verbose_name = gettext_lazy("Category tag")
        verbose_name_plural = gettext_lazy("Category tags")
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("blog:posts_by_tag", args=[self.slug])


class TaggedWithCategoryTags(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CategoryTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_tags",
    )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class FeaturedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .published.filter(is_featured=True)
            .order_by("categories", "featured_order")
        )


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
    tags = TaggableManager(
        through=TaggedWithCategoryTags,
        verbose_name="Category tags",
        help_text="Category tags, comma separated",
    )
    is_featured = models.BooleanField(default=False)
    featured_order = models.IntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()
    featured = FeaturedManager()

    thumbnail = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(200, 200)],
        format="jpeg",
        options={"quality": 60},
    )
    header_image = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(1200, 400)],
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
        self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = self.slug or slugify(self.title)

        if not Post.objects.filter(slug=base_slug).exclude(pk=self.pk).exists():
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

        return slug

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    # parent_comment = models.ForeignKey("self", null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def is_updated(self):
        return self.updated - self.created > timezone.timedelta(minutes=1)

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"


# class FeaturedPost(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     order = models.IntegerField(
#         default=0, help_text="Enter an integer value to define the display order."
#     )

#     class Meta:
#         unique_together = ("post", "category")
#         ordering = ["order"]
