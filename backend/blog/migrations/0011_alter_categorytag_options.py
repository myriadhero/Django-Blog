# Generated by Django 4.2.2 on 2023-06-20 01:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0010_categorytag_is_sub_category_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categorytag",
            options={
                "ordering": ["-is_sub_category", "name"],
                "verbose_name": "Tag with categories",
                "verbose_name_plural": "Tags with categories",
            },
        ),
    ]
