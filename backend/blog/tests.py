from django.contrib.auth import get_user_model
from django.test import TestCase
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
# about page
# admin pages - queries?


class FrontPageTests(TestCase):
    def setUp(self) -> None:
        url = "/"
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "blog/front_page/front_page.html")


class CategorySetUpMixin:
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
            name="DoggoSubcategory", slug="doggo-subcat"
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


class CategoryTests(CategorySetUpMixin, TestCase):
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


class SubategoryTests(CategorySetUpMixin, TestCase):
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


class TagTests(CategorySetUpMixin, TestCase):
    def test_template_used(self):
        url = self.tag.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/list.html")


class SearchTests(CategorySetUpMixin, TestCase):
    def test_template_used(self):
        url = reverse("blog:post_search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/search.html")

        url += f"?query={self.post.title}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/search.html")


class PostTests(CategorySetUpMixin, TestCase):
    def test_template_used(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/detail.html")


class AboutPage(TestCase):
    def setUp(self) -> None:
        url = "/about/"
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "core/about/about.html")
