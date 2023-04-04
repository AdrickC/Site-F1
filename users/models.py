from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from general.models import League, Team
from PIL import Image
from django.db.models import Sum
from bureaufia.models import EventResult



# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Utilisateur', on_delete=models.CASCADE, editable=False)
    image = models.ImageField(verbose_name='Photo de profil', default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.image: 
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'



class License(models.Model):
    profile = models.OneToOneField(Profile, verbose_name='Utilisateur', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name='Ecurie', null=True, on_delete=models.SET_NULL)
    leagues = models.ManyToManyField(League, verbose_name='Ligues')
    status_choices = (
        ('Titulaire', 'Titulaire'),
        ('Remplaçant', 'Remplaçant'),
        ('En attente', 'En attente'),
    )
    status = models.CharField(verbose_name="Statut licence", max_length=50, default='En attente', choices=status_choices)
    total_points = models.PositiveIntegerField(default=0)

    def update_total_points(self):
        self.total_points = EventResult.objects.filter(license=self).aggregate(total_points=Sum('points'))['total_points'] or 0
        self.save()

    def __str__(self):
        return f'{self.profile}'

    class Meta:
        verbose_name = 'Licence'
        verbose_name_plural = 'Licences'



class ChampionshipApplication(models.Model):
    user = models.ForeignKey(User, verbose_name='Utilisateur', on_delete=models.CASCADE)
    first_name = models.CharField('Prénom', max_length=50)
    platform = models.CharField('Plateforme', max_length=50)
    platform_id = models.CharField('Identifiant plateforme', max_length=50)
    availability_choices = (
        ('Vendredi', 'les vendredis de 20h30 à 22h30'),
        ('Dimanche', 'les dimanches de 20h30 à 22h30'),
        ('Vendredi et Dimanche', 'les vendredis et dimanches'),
    )
    availability = models.CharField('Disponibilités', max_length=50, choices=availability_choices)
    teammates = models.CharField('Coéquipiers souhaités', max_length=200)
    preferred_team1 = models.ForeignKey(Team, verbose_name='Ecurie 1 souhaitée', null=True, on_delete=models.SET_NULL, related_name='preferred_team1')
    preferred_team2 = models.ForeignKey(Team, verbose_name='Ecurie 2 souhaitée', null=True, on_delete=models.SET_NULL, related_name='preferred_team2')
    preferred_team3 = models.ForeignKey(Team, verbose_name='Ecurie 3 souhaitée', null=True, on_delete=models.SET_NULL, related_name='preferred_team3')

    class Meta:
        verbose_name = 'Inscription championnat'
        verbose_name_plural = 'Inscriptions championnat'

    def __str__(self):
        return f'{self.user.username} - Demande de championnat'
