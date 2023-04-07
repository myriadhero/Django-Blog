# Generated by Django 4.1.7 on 2023-03-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_post_ttags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["order"]},
        ),
        migrations.AlterModelOptions(
            name="subcategory",
            options={"ordering": ["order"]},
        ),
        migrations.AddField(
            model_name="category",
            name="order",
            field=models.IntegerField(
                default=0,
                help_text="Enter an integer value to define the display order.",
            ),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="order",
            field=models.IntegerField(
                default=0,
                help_text="Enter an integer value to define the display order.",
            ),
        ),
    ]
