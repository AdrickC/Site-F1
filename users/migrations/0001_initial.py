# Generated by Django 4.2 on 2023-05-19 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("general", "0001_initial"),
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
                            ("Titulaire", "Titulaire"),
                            ("Remplaçant", "Remplaçant"),
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
        migrations.CreateModel(
            name="ChampionshipApplication",
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
                ("first_name", models.CharField(max_length=50, verbose_name="Prénom")),
                (
                    "platform",
                    models.CharField(max_length=50, verbose_name="Plateforme"),
                ),
                (
                    "platform_id",
                    models.CharField(
                        max_length=50, verbose_name="Identifiant plateforme"
                    ),
                ),
                (
                    "availability",
                    models.CharField(
                        choices=[
                            ("Vendredi", "les vendredis de 20h30 à 22h30"),
                            ("Dimanche", "les dimanches de 20h30 à 22h30"),
                            ("Vendredi et Dimanche", "les vendredis et dimanches"),
                        ],
                        max_length=50,
                        verbose_name="Disponibilités",
                    ),
                ),
                (
                    "teammates",
                    models.CharField(
                        max_length=200, verbose_name="Coéquipiers souhaités"
                    ),
                ),
                (
                    "preferred_team1",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="preferred_team1",
                        to="general.team",
                        verbose_name="Ecurie 1 souhaitée",
                    ),
                ),
                (
                    "preferred_team2",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="preferred_team2",
                        to="general.team",
                        verbose_name="Ecurie 2 souhaitée",
                    ),
                ),
                (
                    "preferred_team3",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="preferred_team3",
                        to="general.team",
                        verbose_name="Ecurie 3 souhaitée",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Utilisateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "Inscription championnat",
                "verbose_name_plural": "Inscriptions championnat",
            },
        ),
    ]
