from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, CategoryTag, Post

# Create your tests here.
# front page
# category pages, tag list and blog list
# tag page
# all posts page?
# search page
# pagination for all above (except front)
# post detail page
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
        self.cat_tag = CategoryTag.objects.create(name="DoggoTag", slug="doggo-cat-tag")
        self.cat_tag.categories.add(self.cat)

        self.post = Post.objects.create(
            title="doggo post",
            slug="doggo-post",
            body="this is my doggo body",
            status=Post.Status.PUBLISHED,
            author=self.user,
        )
        self.post.categories.add(self.cat)
        self.post.tags.add(self.cat_tag)


class CategoryTests(CategorySetUpMixin, TestCase):
    def test_category_templates_used(self):
        url = self.cat.get_absolute_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/categories/post_tag_list.html")

        self.cat.is_tag_list = True
        self.cat.save()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/categories/tag_list.html")


class TagTests(CategorySetUpMixin, TestCase):
    def test_template_used(self):
        url = self.cat_tag.get_absolute_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/post/list.html")


class PostTests(CategorySetUpMixin, TestCase):
    def test_template_used(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/post/detail.html")


class AboutPage(TestCase):
    def setUp(self) -> None:
        url = "/about/"
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "core/about/about.html")
