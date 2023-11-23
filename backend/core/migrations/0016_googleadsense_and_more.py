# Generated by Django 4.2.7 on 2023-11-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_alter_siteidentity_seo_keywords"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoogleAdsense",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enable_ads",
                    models.BooleanField(
                        default=False,
                        help_text="Enable AdSense ads on the site. Initial verification can be done by meta tag.",
                    ),
                ),
                (
                    "client_id",
                    models.CharField(
                        blank=True,
                        help_text="The ID string from the meta tag or script snippet that starts with 'ca-pub-', include 'ca-pub-' in the field",
                        max_length=100,
                    ),
                ),
                (
                    "enable_google_smart_ads",
                    models.BooleanField(
                        default=False, help_text="Enable google smart ads on the site"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Google Adsense",
            },
        ),
        migrations.AddConstraint(
            model_name="googleadsense",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("enable_ads", False),
                    models.Q(
                        ("client_id__isnull", False),
                        ("client_id__startswith", "ca-pub-"),
                    ),
                    _connector="OR",
                ),
                name="adsense_client_id_required_if_enable_ads",
                violation_error_message="Client ID is required if ads are enabled and should start with 'ca-pub-'",
            ),
        ),
    ]
