# Generated by Django 4.2.2 on 2023-06-19 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0009_remove_dropdownnavitem_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="categorytag",
            name="is_sub_category",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="dropdownnavitem",
            name="category_tag",
            field=models.ForeignKey(
                limit_choices_to={"is_sub_category": True},
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.categorytag",
            ),
        ),
    ]
