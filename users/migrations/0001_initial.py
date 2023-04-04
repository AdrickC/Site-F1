# Generated by Django 4.1.5 on 2023-03-29 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("general", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="profile_pics/default.png",
                        upload_to="profile_pics",
                        verbose_name="Photo de profil",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Utilisateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "Profil",
                "verbose_name_plural": "Profils",
            },
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Actif", "Actif"),
                            ("Inactif", "Inactif"),
                            ("En attente", "En attente"),
                        ],
                        default="En attente",
                        max_length=50,
                        verbose_name="Statut licence",
                    ),
                ),
                ("total_points", models.PositiveIntegerField(default=0)),
                (
                    "leagues",
                    models.ManyToManyField(to="general.league", verbose_name="Ligues"),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.profile",
                        verbose_name="Utilisateur",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="general.team",
                        verbose_name="Ecurie",
                    ),
                ),
            ],
            options={
                "verbose_name": "Licence",
                "verbose_name_plural": "Licences",
            },
        ),
    ]
