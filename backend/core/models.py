from django.db import models

from ckeditor.fields import RichTextField

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

    objects = SingletonManager()

    class Meta:
        verbose_name_plural = "Site Identity"

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
        verbose_name_plural = "About Page"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(AboutPage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return f"About Page - {self.title}"