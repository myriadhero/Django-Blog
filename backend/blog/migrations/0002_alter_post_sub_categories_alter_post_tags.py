# Generated by Django 4.1.7 on 2023-03-19 05:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="sub_categories",
            field=models.ManyToManyField(blank=True, to="blog.subcategory"),
        ),
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(blank=True, to="blog.tag"),
        ),
    ]
