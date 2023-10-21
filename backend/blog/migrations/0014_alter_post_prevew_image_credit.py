# Generated by Django 4.2.5 on 2023-10-21 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0013_post_prevew_image_credit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="prevew_image_credit",
            field=models.CharField(
                blank=True,
                help_text="Consider adding a credit and a link to the source. 500 characters long.",
                max_length=500,
            ),
        ),
    ]
