from core.models import get_site_identity
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Count, Exists, OuterRef
from django.db.models.functions import Collate
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy
from django_ckeditor_5.fields import CKEditor5Field
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from lxml import html
from meta.models import ModelMeta
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase


class FrontPageCatsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(show_on_front_page=True)


class MenuCatsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(show_in_menu=True)


class Category(ModelMeta, models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    slug = models.SlugField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        unique=True,
        help_text="Please use only letters, numbers, underscores or hyphens; must be unique.",
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        help_text="250 characters long, will also be used in SEO description for the page",
    )
    preview_image = models.ImageField(upload_to="category_previews/", blank=True)
    show_on_front_page = models.BooleanField(default=False)
    order = models.IntegerField(
        default=0,
        help_text="Enter an integer value to define the front page carousel section order.",
    )
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

    _metadata = {
        "title": "get_seo_title",
        "description": "get_seo_description",
        "keywords": "get_seo_keywords",
        "image": "get_preview_image_url",
        "og_type": "Website",
        "object_type": "Website",
    }

    objects = models.Manager()
    on_front_page = FrontPageCatsManager()

    class Meta:
        ordering = ["order"]
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

    def get_seo_title(self):
        return get_site_identity().get_title_and_tagline(page_name=self.name)

    def get_seo_description(self):
        return self.description or f"{'Tags from' if self.is_tag_list else 'Posts about'} {self.name}."

    def get_seo_keywords(self):
        return [self.name.lower()] + (get_site_identity().get_seo_keywords() or [])

    def get_preview_image_url(self):
        return self.thumbnail.url if self.preview_image else None

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])


class Subcategory(ModelMeta, models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    slug = models.SlugField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        unique=True,
        help_text="Please use only letters, numbers, underscores or hyphens; must be unique.",
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        help_text="250 characters long, will also be used in SEO description for the page",
    )
    preview_image = models.ImageField(upload_to="category_previews/", blank=True)
    categories = models.ManyToManyField(Category, related_name="subcategories")

    thumbnail = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(200, 200)],
        format="jpeg",
        options={"quality": 60},
    )

    _metadata = {
        "title": "get_seo_title",
        "description": "get_seo_description",
        "keywords": "get_seo_keywords",
        "image": "get_preview_image_url",
        "og_type": "Website",
        "object_type": "Website",
    }

    class Meta:
        verbose_name = gettext_lazy("Subcategory")
        verbose_name_plural = gettext_lazy("Subcategories")

    def get_tags_that_have_at_least_one_post(self):
        post_content_type = ContentType.objects.get_for_model(Post)
        tag_relations = TaggedWithCategoryTags.objects.filter(
            tag=OuterRef("pk"),
            content_type=post_content_type,
            object_id__in=self.post_set.all(),
        )
        return self.categorytag_set.filter(Exists(tag_relations))

    def get_seo_title(self):
        return get_site_identity().get_title_and_tagline(page_name=self.name)

    def get_seo_description(self):
        return self.description or f"Posts about {self.name}."

    def get_seo_keywords(self):
        return (
            [self.name.lower()]
            + [cat.name.lower() for cat in self.categories.all()]
            + (get_site_identity().get_seo_keywords() or [])
        )

    def get_preview_image_url(self):
        return self.thumbnail.url if self.preview_image else None

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self, **kwargs):
        if not ((category := kwargs.get("category")) or (category_slug := kwargs.get("category_slug"))):
            return reverse("blog:subcategory", args=[self.slug])

        category = category or Category.objects.filter(slug=category_slug).first()

        return reverse(
            "blog:category_subcategory",
            args=[category.slug, self.slug],
        )


class NonEmptyTagsManager(models.Manager):
    def get_queryset(self):
        tag_relations = TaggedWithCategoryTags.objects.filter(
            tag=OuterRef("pk"),
        )
        return super().get_queryset().filter(Exists(tag_relations))


class CategoryTag(ModelMeta, TagBase):
    description = models.CharField(
        max_length=250,
        blank=True,
        help_text="250 characters long, can also be used in SEO description for the page",
    )
    preview_image = models.ImageField(upload_to="tag_previews/", blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    subcategories = models.ManyToManyField(Subcategory, blank=True)

    thumbnail = ImageSpecField(
        source="preview_image",
        processors=[ResizeToFill(200, 200)],
        format="jpeg",
        options={"quality": 60},
    )

    _metadata = {
        "title": "get_seo_title",
        "description": "get_seo_description",
        "keywords": "get_seo_keywords",
        "image": "get_preview_image_url",
        "og_type": "Website",
        "object_type": "Website",
    }

    objects = models.Manager()
    non_empty = NonEmptyTagsManager()

    class Meta:
        verbose_name = gettext_lazy("Tag")
        verbose_name_plural = gettext_lazy("Tags")
        ordering = (Collate("slug", "C"),)

    def get_seo_title(self):
        return get_site_identity().get_title_and_tagline(page_name=self.name)

    def get_seo_description(self):
        return self.description or f"Posts with {self.name} tag."

    def get_seo_keywords(self):
        return (
            [self.name.lower()]
            + [cat.name.lower() for cat in self.categories.all()]
            + [subcat.name.lower() for subcat in self.subcategories.all()]
            + (get_site_identity().get_seo_keywords() or [])
        )

    def get_preview_image_url(self):
        return self.thumbnail.url if self.preview_image else None

    def get_absolute_url(self):
        return reverse("blog:posts_by_tag", args=[self.slug])

    def get_tagged_posts(self):
        return Post.objects.filter(tags=self)


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

    def get_absolute_url(self):
        return self.primary_category.get_absolute_url()


class DropdownNavItem(models.Model):
    parent_nav_item = models.ForeignKey(
        NavItem,
        on_delete=models.CASCADE,
        related_name="sub_items",
    )
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.parent_nav_item.primary_category.name} Nav Dropdown - {self.subcategory.name} subcategory"

    def get_absolute_url(self):
        return self.subcategory.get_absolute_url(
            category=self.parent_nav_item.primary_category,
        )


class TaggedWithCategoryTags(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CategoryTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_tags",
    )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(ModelMeta, models.Model):
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
    description = models.CharField(
        max_length=250,
        blank=True,
        help_text="Used for SEO, typically 60-150 chars long but up to 250 is fine. Title is used if left blank.",
    )
    preview_image = models.ImageField(upload_to="blog_previews/", blank=True)
    prevew_image_credit = models.CharField(
        max_length=500,
        blank=True,
        help_text="Consider adding a credit and a link to the source. 500 characters long.",
    )
    body = CKEditor5Field()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    categories = models.ManyToManyField(Category)
    subcategories = models.ManyToManyField(Subcategory, blank=True)
    tags = TaggableManager(
        through=TaggedWithCategoryTags,
        help_text="Tags, comma separated",
    )
    _metadata = {
        "title": "get_seo_title",
        "description": "get_seo_description",
        "keywords": "get_seo_keywords",
        "image": "get_preview_image_url",
        "og_type": "Article",
        "object_type": "Article",
    }

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
        ordering = ("-publish",)
        indexes = (models.Index(fields=["-publish"]),)

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        self.remove_scripts_from_body()
        self.check_youtube_iframe()
        super().save(*args, **kwargs)

    def get_similar_posts(self, post_num=5):
        post_tags_ids = self.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=self.id,
        )

        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags",
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

    def get_seo_title(self):
        return get_site_identity().get_title_and_tagline(page_name=self.title)

    def get_seo_description(self):
        return self.description or self.title

    def get_seo_keywords(self):
        return (
            [cat.name.lower() for cat in self.categories.all()]
            + [tag.name.lower() for tag in self.tags.all()]
            + (get_site_identity().get_seo_keywords() or [])
        )

    def get_preview_image_url(self):
        return self.thumbnail.url if self.preview_image else None

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __str__(self) -> str:
        return self.title


class FeaturedPostPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(post__status=Post.Status.PUBLISHED)


class FeaturedPost(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="featured_posts",
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField(
        default=0,
        help_text="Enter an integer value to define the display order.",
    )

    objects = models.Manager()
    published = FeaturedPostPublishedManager()

    class Meta:
        unique_together = ("category", "post")
        ordering = ("order", "-post__publish")

    def __str__(self):
        return f"{self.category} - {self.post} (Order: {self.order}, Published: {self.post.publish.strftime('%a %d %b %Y, %I:%M%p')})"
