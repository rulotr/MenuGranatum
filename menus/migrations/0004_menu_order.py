# Generated by Django 4.2.13 on 2024-05-23 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0003_alter_menu_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="order",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]