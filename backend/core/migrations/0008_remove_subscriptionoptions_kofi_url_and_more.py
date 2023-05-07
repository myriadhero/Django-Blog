# Generated by Django 4.2 on 2023-05-07 04:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_subscriptionoptions_show_kofi_link_in_head_menu_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscriptionoptions",
            name="kofi_url",
        ),
        migrations.AlterField(
            model_name="subscriptionoptions",
            name="show_kofi_form_in_footer",
            field=models.BooleanField(
                default=False, help_text="Shows kofi form in footer"
            ),
        ),
        migrations.AlterField(
            model_name="subscriptionoptions",
            name="show_kofi_link_in_head_menu",
            field=models.BooleanField(
                default=False, help_text="Shows kofi icon and link in the top site menu"
            ),
        ),
        migrations.AlterField(
            model_name="subscriptionoptions",
            name="show_kofi_overlay_button",
            field=models.BooleanField(
                default=False, help_text="Shows kofi overlap button"
            ),
        ),
    ]
