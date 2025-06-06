# Generated by Django 5.2 on 2025-04-26 03:07

import django.db.models.functions.comparison
import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_categorytag_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorytag',
            options={'ordering': (django.db.models.functions.comparison.Collate('slug', 'C'),), 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='featuredpost',
            options={'ordering': ('order', '-post__publish')},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',)},
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
