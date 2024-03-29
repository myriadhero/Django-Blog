# Generated by Django 4.2.6 on 2023-11-01 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_siteidentity_carousel_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteidentity",
            name="seo_description",
            field=models.TextField(
                blank=True,
                help_text="Used in SEO meta tags, should be 50-160 characters long",
            ),
        ),
    ]
