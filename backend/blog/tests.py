import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, CategoryTag, Post, Subcategory

# Create your tests here.
# front page
# category pages, filter by subcategories and tags
# subcategory pages, filter by tags
# tag page
# all posts page
# post detail page
# search page
# pagination for all above (except front and detail)
# admin pages
# image fields


class FrontPageTests(TestCase):
    def setUp(self) -> None:
        url = "/"
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "blog/front_page/front_page.html")


class CommonSetUpMixin:
    def setUp(self):
        super().setUp()
        username = "doggobloggersson"
        email = "dogoo@gmail.com"
        password = "doggopass123"
        User = get_user_model()
        self.user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        self.cat = Category.objects.create(name="DoggoCategory", slug="doggocat")
        self.subcat = Subcategory.objects.create(
            name="DoggoSubcategory",
            slug="doggo-subcat",
        )
        self.subcat.categories.add(self.cat)
        self.tag = CategoryTag.objects.create(name="DoggoTag", slug="doggo-cat-tag")
        self.tag.categories.add(self.cat)
        self.tag.subcategories.add(self.subcat)

        self.post = Post.objects.create(
            title="doggo post",
            slug="doggo-post",
            body="this is my doggo body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )
        self.post.categories.add(self.cat)
        self.post.tags.add(self.tag)


class CategoryTests(CommonSetUpMixin, TestCase):
    def test_category_templates_used(self):
        url = self.cat.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/categories/category_post_list.html")

        self.cat.is_tag_list = True
        self.cat.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/categories/tag_list.html")


class SubategoryTests(CommonSetUpMixin, TestCase):
    def test_category_templates_used(self):
        url = self.subcat.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/categories/subcategory_post_list.html")

        url = self.subcat.get_absolute_url(category_slug=self.cat.slug)
        assert self.cat.slug in url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/categories/subcategory_post_list.html")


class TagTests(CommonSetUpMixin, TestCase):
    def test_template_used(self):
        url = self.tag.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/list.html")


class SearchTests(CommonSetUpMixin, TestCase):
    def test_template_used(self):
        url = reverse("blog:post_search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/search.html")

        url += f"?query={self.post.title}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/search.html")


class PostTests(CommonSetUpMixin, TestCase):
    def test_template_used(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_draft_post_detail_view_anonymous(self):
        draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            body="This is a draft",
            status=Post.Status.DRAFT,
            author=self.user,
        )
        url = reverse("blog:post_detail", args=[draft_post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_draft_post_preview_view_logged_in(self):
        draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            body="This is a draft",
            status=Post.Status.DRAFT,
            author=self.user,
        )
        self.client.login(username="doggobloggersson", password="doggopass123")
        url = reverse("blog:post_detail_preview", args=[draft_post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_draft_post_preview_view_anonymous_redirects(self):
        draft_post = Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            body="This is a draft",
            status=Post.Status.DRAFT,
            author=self.user,
        )
        url = reverse("blog:post_detail_preview", args=[draft_post.slug])
        response = self.client.get(url)
        expected_redirect = f"/accounts/login/?next={url}"
        self.assertRedirects(response, expected_redirect, fetch_redirect_response=False)

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_preview_image_shown_based_on_conditions(self):
        small_gif = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"

        # Post with image and show=True (Left position, default)
        post_with = Post.objects.create(
            title="Post with image show true",
            slug="post-with-image-show",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
            show_preview_image=True,
        )
        post_with.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        post_with.save()
        response = self.client.get(post_with.get_absolute_url())
        self.assertContains(response, 'class="image is-3by4 post-preview"')
        self.assertNotContains(response, 'class="block post-preview image is-16by9"')

        # Post with image and show=True, position=Top
        post_top = Post.objects.create(
            title="Post with image show true top",
            slug="post-with-image-show-top",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
            show_preview_image=True,
            preview_image_position=Post.PreviewPosition.TOP,
        )
        post_top.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        post_top.save()
        response = self.client.get(post_top.get_absolute_url())
        self.assertContains(response, 'class="block post-preview image is-16by9"')
        self.assertNotContains(response, 'class="image is-3by4 post-preview"')

        # Post with image but show=False
        post_no_show = Post.objects.create(
            title="Post with image show false",
            slug="post-with-image-no-show",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
            show_preview_image=False,
            preview_image_position=Post.PreviewPosition.TOP,
        )
        post_no_show.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        post_no_show.save()
        response = self.client.get(post_no_show.get_absolute_url())
        self.assertNotContains(response, "image is-3by4 post-preview")
        self.assertNotContains(response, "block post-preview image is-16by9")

        # Post without image but show=True
        post_no_image = Post.objects.create(
            title="Post no image show true",
            slug="post-no-image-show",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
            show_preview_image=True,
            preview_image_position=Post.PreviewPosition.LEFT,
        )
        response = self.client.get(post_no_image.get_absolute_url())
        self.assertNotContains(response, "image is-3by4 post-preview")
        self.assertNotContains(response, "block post-preview image is-16by9")

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_recommended_and_latest_posts_only_show_posts_with_images(self):
        small_gif = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"

        # Main post
        main_post = Post.objects.create(
            title="Main Post",
            slug="main-post",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )
        main_post.tags.add(self.tag)

        # Similar post with image
        similar_with_image = Post.objects.create(
            title="Similar with Image",
            slug="similar-with-image",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )
        similar_with_image.tags.add(self.tag)
        similar_with_image.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        similar_with_image.save()

        similar_with_image_draft = Post.objects.create(
            title="Similar with Image Draft",
            slug="similar-with-image-draft",
            body="body",
            status=Post.Status.DRAFT,
            author=self.user,
        )
        similar_with_image_draft.tags.add(self.tag)
        similar_with_image_draft.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        similar_with_image_draft.save()

        # Similar post without image
        similar_without_image = Post.objects.create(
            title="Similar without Image",
            slug="similar-without-image",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )
        similar_without_image.tags.add(self.tag)

        # Latest post with image (not similar)
        latest_with_image = Post.objects.create(
            title="Latest with Image",
            slug="latest-with-image",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )
        latest_with_image.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        latest_with_image.save()

        latest_with_image_draft = Post.objects.create(
            title="Latest with Image Draft",
            slug="latest-with-image-draft",
            body="body",
            status=Post.Status.DRAFT,
            author=self.user,
        )
        latest_with_image_draft.preview_image = SimpleUploadedFile("small.gif", small_gif, "image/gif")
        latest_with_image_draft.save()

        # Latest post without image (not similar)
        latest_without_image = Post.objects.create(
            title="Latest without Image",
            slug="latest-without-image",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )

        response = self.client.get(main_post.get_absolute_url())

        # Check related posts (similar)
        self.assertContains(response, similar_with_image.title)
        self.assertNotContains(response, similar_without_image.title)
        self.assertNotContains(response, similar_with_image_draft.title)

        # Check latest posts
        self.assertContains(response, latest_with_image.title)
        self.assertNotContains(response, latest_without_image.title)
        self.assertNotContains(response, latest_with_image_draft.title)

    def test_post_tags_are_sorted_by_slug(self):
        post = Post.objects.create(
            title="Post",
            slug="post",
            body="body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )

        tag4 = CategoryTag.objects.create(name="Tag 4", slug="tag-4")
        tag3 = CategoryTag.objects.create(name="Tag 3", slug="tag-3")
        tag2 = CategoryTag.objects.create(name="Tag 2", slug="tag-2-1")
        tag1 = CategoryTag.objects.create(name="Tag 1", slug="tag-1")
        tag5 = CategoryTag.objects.create(name="Tag 5", slug="tag-5")
        tag6 = CategoryTag.objects.create(name="Tag 6", slug="tag-6")
        tag7 = CategoryTag.objects.create(name="Tag 7", slug="ctag-7")
        tag8 = CategoryTag.objects.create(name="Tag 8", slug="dtag-8")
        tag9 = CategoryTag.objects.create(name="Tag 9", slug="btag-9")
        tag10 = CategoryTag.objects.create(name="Tag 10", slug="atag-10")

        post.tags.add(*[tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9, tag10])
        post.tags.add(self.tag)
        post.save()

        self.assertEqual(
            [(t.id, t.slug) for t in post.tags.all()],
            [
                (tag10.id, "atag-10"),
                (tag9.id, "btag-9"),
                (tag7.id, "ctag-7"),
                (self.tag.id, "doggo-cat-tag"),
                (tag8.id, "dtag-8"),
                (tag1.id, "tag-1"),
                (tag2.id, "tag-2-1"),
                (tag3.id, "tag-3"),
                (tag4.id, "tag-4"),
                (tag5.id, "tag-5"),
                (tag6.id, "tag-6"),
            ],
        )
        self.assertEqual(
            [*post.tags.order_by("name").all()],
            [self.tag, tag1, tag10, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9],
        )
