from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy


# Create your models here.
class SingletonManager(models.Manager):
    def get_instance(self):
        instance, created = self.get_or_create(pk=1)
        return instance


class SiteIdentity(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="site_identity/", blank=True)
    favicon = models.ImageField(upload_to="site_identity/", blank=True)
    footer = RichTextField(blank=True)
    header_message = models.RichTextField(blank=True)

    objects = SingletonManager()

    class Meta:
        verbose_name_plural = gettext_lazy("Site Identity")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteIdentity, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return f"Site Identity - {self.title}"


class AboutPage(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()

    objects = SingletonManager()

    class Meta:
        verbose_name_plural = gettext_lazy("About Page")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(AboutPage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return f"About Page - {self.title}"


class SubscriptionOptions(models.Model):
    kofi_account_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Is the name at the end of the URL without the URL stuff",
    )
    show_kofi_link_in_head_menu = models.BooleanField(
        default=False,
        help_text="Shows kofi icon and link in the top site menu",
    )
    show_kofi_form_in_footer = models.BooleanField(
        default=False,
        help_text="Shows kofi form in footer",
    )
    show_kofi_overlay_button = models.BooleanField(
        default=False,
        help_text="Shows kofi overlap button",
    )

    objects = SingletonManager()

    class Meta:
        verbose_name_plural = gettext_lazy("Subscription Options")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SubscriptionOptions, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def clean(self):
        if (
            self.show_kofi_form_in_footer
            or self.show_kofi_overlay_button
            or self.show_kofi_link_in_head_menu
        ) and not self.kofi_account_name:
            raise ValidationError(
                "Kofi account name is required to turn on kofi widgets"
            )
        return super().clean()

    def __str__(self):
        return "Subscription Options"


class SocialMedia(models.Model):
    class Meta:
        verbose_name_plural = gettext_lazy("Social Media")

    youtube_url = models.URLField(blank=True)
    youtube_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Shown in the mobile menu",
    )
    twitter_url = models.URLField(blank=True)
    twitter_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Shown in the mobile menu",
    )

    objects = SingletonManager()

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SocialMedia, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return "Social Media"
