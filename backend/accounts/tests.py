from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import UserProfile

User = get_user_model()


class UserProfileSignalTests(TestCase):
    def test_profile_created_when_user_is_created(self):
        user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="secret123",
        )

        self.assertTrue(UserProfile.objects.filter(user=user).exists())

        profile = user.profile  # should be available due to signal
        self.assertEqual(str(profile), f"{user.username} profile")

    def test_profile_not_duplicated_on_user_update(self):
        user = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="secret123",
        )

        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

        user.first_name = "Bobby"
        user.save()

        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)
