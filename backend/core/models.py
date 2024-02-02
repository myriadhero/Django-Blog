from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from meta.models import ModelMeta


class SingletonManager(models.Manager):
    def get_instance(self):
        instance, created = self.get_or_create(pk=1)
        return instance


class SiteIdentity(ModelMeta, models.Model):
    title = models.CharField(max_length=100, help_text="Limit this to just the site name, eg 'SiteName'")
    tagline = models.CharField(
        max_length=250,
        blank=True,
        help_text="This is appended to site title in the browser tab",
    )
    seo_description = models.TextField(
        blank=True, help_text="Used in SEO meta tags, should be 50-160 characters long",
    )
    seo_keywords = models.CharField(
        max_length=250,
        blank=True,
        help_text="List of words in SEO meta tags, eg 'blog, django, python' without quotes, comma separated",
    )
    logo_title = models.ImageField(
        upload_to="site_identity/", blank=True, help_text="Used for the main top logo",
    )
    logo_square = models.ImageField(
        upload_to="site_identity/",
        blank=True,
        help_text="Used for seo and other places where a square logo is needed",
    )
    favicon = models.ImageField(upload_to="site_identity/", blank=True)
    # TODO: validate svg/images
    carousel_logo = models.FileField(
        upload_to="site_identity/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "svg", "gif"]),
        ],
        help_text="This logo is used as a placeholder pic for carousel cards. Can be jpg png svg gif, use .svg for best fit, do not upload untrusted files!",
    )
    footer = RichTextField(blank=True, help_text="Goes above the copyright message")
    footer_copy_message = models.CharField(max_length=250, blank=True, help_text="Goes next to copyright eg \"© SiteName Year - Message\"")
    header_message = models.TextField(
        blank=True,
        help_text="Adds a message to the top of the site on all pages. Change to blank to remove the message.",
    )

    thumbnail_title = ImageSpecField(
        source="logo_title",
        processors=[ResizeToFill(200, 100)],
        format="png",
        options={"quality": 60},
    )
    thumbnail_square = ImageSpecField(
        source="logo_square",
        processors=[ResizeToFill(200, 200)],
        format="png",
        options={"quality": 60},
    )
    _metadata = {
        "title": "get_title_and_tagline",
        "description": "seo_description",
        "keywords": "get_seo_keywords",
        "image": "get_logo_square_url",
        "og_type": "Website",
        "object_type": "Website",
    }

    objects = SingletonManager()

    class Meta:
        verbose_name_plural = gettext_lazy("Site Identity")

    def __str__(self):
        return f"Site Identity - {self.title}"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteIdentity, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def get_title_and_tagline(self, page_name=None):
        return f"{self.title}{' - ' + page_name if page_name else ''}{' - '+ self.tagline if self.tagline else ''}"

    def get_logo_square_url(self):
        return self.logo_square.url if self.logo_square else None

    def get_seo_keywords(self):
        return (
            [
                stripped_word
                for word in self.seo_keywords.split(",")
                if (stripped_word := word.strip())
            ]
            if self.seo_keywords
            else None
        )


def get_site_identity() -> SiteIdentity:
    return SiteIdentity.objects.get_instance()


class AboutPage(ModelMeta, models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()

    objects = SingletonManager()

    _metadata = {
        "title": "get_title",
        "description": "get_seo_description",
        "keywords": "get_seo_keywords",
        "image": "get_logo_square_url",
        "og_type": "Website",
        "object_type": "Website",
    }

    class Meta:
        verbose_name_plural = gettext_lazy("About Page")

    def __str__(self):
        return f"About Page - {self.title}"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(AboutPage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def get_title(self):
        return get_site_identity().get_title_and_tagline(page_name=self.title)

    def get_logo_square_url(self):
        return get_site_identity().get_logo_square_url()

    def get_seo_keywords(self):
        return get_site_identity().get_seo_keywords()

    def get_seo_description(self):
        return get_site_identity().seo_description


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

    def __str__(self):
        return "Subscription Options"

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
                "Kofi account name is required to turn on kofi widgets",
            )
        return super().clean()


class SocialMedia(models.Model):


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
    class Meta:
        verbose_name_plural = gettext_lazy("Social Media")

    def __str__(self):
        return "Social Media"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SocialMedia, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class GoogleAdsense(models.Model):
    enable_ads = models.BooleanField(
        default=False,
        help_text="Enable AdSense ads on the site. Initial verification can be done by meta tag.",
    )
    client_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="The ID string from the meta tag or script snippet that starts with 'ca-pub-', include 'ca-pub-' in the field",
    )
    enable_google_smart_ads = models.BooleanField(
        default=False,
        help_text="Enable google smart ads on the site",
    )

    objects = SingletonManager()

    class Meta:
        verbose_name_plural = gettext_lazy("Google Adsense")
        constraints = (
            models.CheckConstraint(
                check=models.Q(enable_ads=False)
                | (
                    models.Q(client_id__isnull=False)
                    & models.Q(client_id__startswith="ca-pub-")
                ),
                name="adsense_client_id_required_if_enable_ads",
                violation_error_message="Client ID is required if ads are enabled and should start with 'ca-pub-'",
            ),
        )

    def __str__(self):
        return "Google Adsense"
