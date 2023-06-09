# Generated by Django 4.2 on 2023-04-28 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_category_description_category_preview_image_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FeaturedPost",
        ),
        migrations.RemoveField(
            model_name="post",
            name="featured_order",
        ),
        migrations.RemoveField(
            model_name="post",
            name="is_featured",
        ),
        migrations.CreateModel(
            name="FeaturedPost",
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
                    "order",
                    models.IntegerField(
                        default=0,
                        help_text="Enter an integer value to define the display order.",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="featured_posts",
                        to="blog.category",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.post"
                    ),
                ),
            ],
            options={
                "ordering": ["order", "-post__publish"],
                "unique_together": {("category", "post")},
            },
        ),
    ]
