# Generated by Django 5.0 on 2024-01-22 06:27

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_googleadsense_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteidentity",
            name="footer_copy_message",
            field=models.CharField(
                blank=True,
                help_text='Goes next to copyright eg "© SiteName Year - Message"',
                max_length=250,
            ),
        ),
        migrations.AlterField(
            model_name="siteidentity",
            name="footer",
            field=ckeditor.fields.RichTextField(
                blank=True, help_text="Goes above the copyright message"
            ),
        ),
    ]
