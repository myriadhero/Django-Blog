from django.contrib.auth import get_user_model
from django.db import models
from imagefield.fields import ImageField

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = ImageField(
        upload_to="user_avatars",
        blank=True,
        formats={
            "thumb": ["default", ("crop", (96, 96))],
        },
        auto_add_fields=True,
    )

    def __str__(self):
        return f"{self.user.username} profile"
