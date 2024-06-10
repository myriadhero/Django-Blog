from django import forms
from django.db import models


# Create your models here.
class Feedback(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Anonymous"
        # TODO: add bleach to clean the message?
        super().save(*args, **kwargs)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("message", "name", "email")
