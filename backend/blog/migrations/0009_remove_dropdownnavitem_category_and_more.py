# Generated by Django 4.2.2 on 2023-06-19 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_alter_navitem_primary_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dropdownnavitem",
            name="category",
        ),
        migrations.AddField(
            model_name="dropdownnavitem",
            name="category_tag",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.categorytag",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dropdownnavitem",
            name="parent_nav_item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sub_items",
                to="blog.navitem",
            ),
        ),
    ]
