# Generated by Django 4.1.5 on 2023-03-30 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="circuit",
            name="version",
        ),
    ]