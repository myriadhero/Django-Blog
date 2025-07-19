from django.test import TestCase


# about page
# terms page
# subscriptions
# social media and adsence
# site identity

class AboutPage(TestCase):
    def setUp(self) -> None:
        url = "/about/"
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "core/about/about.html")


class TermsPage(TestCase):
    def setUp(self) -> None:
        url = "/terms-of-service/"
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "core/about/terms.html")
