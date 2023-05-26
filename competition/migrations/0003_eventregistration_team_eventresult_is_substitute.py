# Generated by Django 4.2 on 2023-05-23 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0002_game_slug"),
        ("competition", "0002_alter_scoringrule_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventregistration",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="general.team",
                verbose_name="Equipe",
            ),
        ),
        migrations.AddField(
            model_name="eventresult",
            name="is_substitute",
            field=models.BooleanField(default=False),
        ),
    ]