# Generated by Django 4.2 on 2023-04-06 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0002_remove_circuit_version"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Platform",
        ),
    ]