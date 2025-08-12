from django.contrib.auth.models import User
from django.http import HttpResponse as HTTPResponse
from django.test import TestCase

from .models import AboutPage, PrivacyPage, SiteIdentity, TermsPage

# about page
# terms page
# subscriptions
# social media and adsence
# site identity


class AboutPageTests(TestCase):
    def setUp(self) -> None:
        self.url = "/about/"
        self.about = AboutPage.objects.get_instance()
        self.about.title = "Unique title to test for"
        self.about.save()
        self.response = self.client.get(self.url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template_is_used(self):
        self.assertTemplateUsed(self.response, "core/about/about.html")

    def test_title_not_shown_when_disabled(self):
        self.response = self.client.get(self.url)
        self.assertContains(self.response, f'<h1 class="title is-1 has-text-centered">{self.about.title}</h1>')

        self.about.show_title_in_page = False
        self.about.save()
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, f'<h1 class="title is-1 has-text-centered">{self.about.title}</h1>')
        # still contains title in page meta
        self.assertContains(self.response, self.about.title)


class TermsPageTests(TestCase):
    def setUp(self) -> None:
        self.url = "/terms-of-service/"
        self.site_identity = SiteIdentity.objects.get_instance()
        self.terms = TermsPage.objects.get_instance()
        self.staff_user = User.objects.create_user(username="staff", password="testpass")
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_not_enabled_anonymous_404(self):
        self.site_identity.show_terms_of_service = False
        self.site_identity.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_not_enabled_staff_200(self):
        self.site_identity.show_terms_of_service = False
        self.site_identity.save()
        self.client.login(username="staff", password="testpass")
        response: HTTPResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_enabled_anonymous_200(self):
        self.site_identity.show_terms_of_service = True
        self.site_identity.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_is_used(self):
        self.site_identity.show_terms_of_service = True
        self.site_identity.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/about/terms.html")

    def test_default_title_when_empty(self):
        self.site_identity.show_terms_of_service = True
        self.site_identity.save()
        self.terms.title = ""
        self.terms.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertContains(response, "Terms of Service")


class PrivacyPageTests(TestCase):
    def setUp(self) -> None:
        self.url = "/privacy-policy/"
        self.site_identity = SiteIdentity.objects.get_instance()
        self.privacy = PrivacyPage.objects.get_instance()
        self.staff_user = User.objects.create_user(username="staff", password="testpass")
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_not_enabled_anonymous_404(self):
        self.site_identity.show_privacy_policy = False
        self.site_identity.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_not_enabled_staff_200(self):
        self.site_identity.show_privacy_policy = False
        self.site_identity.save()
        self.client.login(username="staff", password="testpass")
        response: HTTPResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_enabled_anonymous_200(self):
        self.site_identity.show_privacy_policy = True
        self.site_identity.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_is_used(self):
        self.site_identity.show_privacy_policy = True
        self.site_identity.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertTemplateUsed(response, "core/about/privacy.html")

    def test_default_title_when_empty(self):
        self.site_identity.show_privacy_policy = True
        self.site_identity.save()
        self.privacy.title = ""
        self.privacy.save()
        response: HTTPResponse = self.client.get(self.url)
        self.assertContains(response, "Privacy Policy")
