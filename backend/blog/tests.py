from django.test import TestCase

# Create your tests here.
# front page
# category pages, tag list and blog list
# tag page
# all posts page
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