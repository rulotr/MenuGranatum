# Generated by Django 4.2.13 on 2024-05-21 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="path",
            field=models.CharField(default="", max_length=50),
        ),
    ]