from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Subscription(models.Model):
    class Frequency(models.TextChoices):
        INSTANT = "I", _("Instant")
        DAILY = "D", _("Daily")
        WEEKLY = "W", _("Weekly")

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    # TODO: decide whether this is a best practice and secure:
    # should i have a permanent identifier for the subscription, or should it be rotated?
    manage_slug = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    frequency = models.CharField(max_length=1, choices=Frequency.choices, default=Frequency.WEEKLY)

    def __str__(self):
        return f"{self.email} - {self.frequency}, {self.created_at} {self.confirmed}"

    def get_absolute_url(self):
        return reverse("manage_subscription", kwargs={"manage_slug": self.manage_slug})

    def confirm(self):
        self.confirmed = True
        self.save()

    @classmethod
    def get_by_manage_slug(cls, manage_slug):
        return cls.objects.get(manage_slug=manage_slug)
