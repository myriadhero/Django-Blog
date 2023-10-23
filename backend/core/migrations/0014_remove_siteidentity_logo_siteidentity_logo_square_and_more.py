# Generated by Django 4.2.6 on 2023-11-01 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_siteidentity_seo_keywords"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="siteidentity",
            name="logo",
        ),
        migrations.AddField(
            model_name="siteidentity",
            name="logo_square",
            field=models.ImageField(
                blank=True,
                help_text="Used for seo and other places where a square logo is needed",
                upload_to="site_identity/",
            ),
        ),
        migrations.AddField(
            model_name="siteidentity",
            name="logo_title",
            field=models.ImageField(
                blank=True,
                help_text="Used for the main top logo",
                upload_to="site_identity/",
            ),
        ),
    ]