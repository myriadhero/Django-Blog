# Generated by Django 5.0 on 2024-01-23 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_siteidentity_footer_copy_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteidentity',
            name='tagline',
            field=models.CharField(blank=True, help_text='This is appended to site title in the browser tab', max_length=250),
        ),
        migrations.AlterField(
            model_name='siteidentity',
            name='title',
            field=models.CharField(help_text="Limit this to just the site name, eg 'SiteName'", max_length=100),
        ),
    ]
