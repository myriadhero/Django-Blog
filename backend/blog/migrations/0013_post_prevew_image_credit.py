# Generated by Django 4.2.5 on 2023-10-21 05:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0012_alter_category_name_alter_category_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="prevew_image_credit",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
