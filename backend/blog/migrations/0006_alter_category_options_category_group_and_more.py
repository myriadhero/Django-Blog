# Generated by Django 4.2.2 on 2023-06-16 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_delete_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["group", "order"],
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AddField(
            model_name="category",
            name="group",
            field=models.IntegerField(
                default=0,
                help_text="Enter an integer value to define the display group order. Categories are sorted and divided by group first, then order within group.",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="order",
            field=models.IntegerField(
                default=0,
                help_text="Enter an integer value to define the display order within a group.",
            ),
        ),
    ]
