# Generated by Django 5.2 on 2025-04-26 03:07

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_siteidentity_tagline_alter_siteidentity_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
        migrations.AlterField(
            model_name='siteidentity',
            name='footer',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, help_text='Goes above the copyright message'),
        ),
    ]
