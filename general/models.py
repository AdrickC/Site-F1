from django.db import models
from pays import Countries
from PIL import Image


# Circuits

country_choices = []
for country in Countries():
    country_choices.append((str(country),str(country)))
country_choices = sorted(country_choices)

circuit_version_choices = (
    ('Grand-Prix', 'Grand-Prix'),
    ('Endurance', 'Endurance')
)

class Circuit(models.Model):
    name = models.CharField('Circuit', max_length=120)
    country = models.CharField('Pays', max_length=120, choices=country_choices)
    image = models.ImageField('Image noir/blanc', blank=True, upload_to='circuit_pics', default='#')
    image_details = models.ImageField('Image détaillée', blank=True, upload_to='circuit_details', default='#')

    def __str__(self):
        return self.name


# Plateformes

class Platform(models.Model):
    platform = models.CharField('Plateforme', max_length=100)
    logo = models.ImageField('Logo', blank=True, upload_to='platform_logos')

    def __str__(self):
        return self.platform

    class Meta:
        verbose_name = 'Plateforme'
        verbose_name_plural = 'Plateformes'


# Jeux

class Game(models.Model):
    name = models.CharField('Nom du jeu', max_length=100)
    logo = models.ImageField('Logo', blank=True, upload_to='game_logos')

    #def incoming_events(self):
        #return self.event_set.filter(event_date__gte = datetime.today()).order_by('event_date')

    #def passed_events(self):
        #return self.event_set.filter(event_date__lt = datetime.today()).order_by('-event_date')[:3]


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Jeu'
        verbose_name_plural = 'Jeux'


# Ecuries

class Team(models.Model):
    team = models.CharField('Ecurie', max_length=120)
    game = models.ForeignKey(Game, verbose_name='Jeu', null=True, on_delete=models.SET_NULL)
    logo = models.ImageField('Logo', blank=True, upload_to='team_logos')

    def __str__(self):
        return self.team

    def save(self, *args, **kwargs):
        super(Team, self).save(*args, **kwargs)

        if self.logo: 
            img = Image.open(self.logo.path)

            if img.height > 40 or img.width > 40:
                output_size = (40,40)
                img.thumbnail(output_size)
                img.save(self.logo.path)

    class Meta:
        verbose_name = 'Ecurie'
        verbose_name_plural = 'Ecuries'


# Ligues F1

class League(models.Model):
    game = models.ForeignKey(Game, verbose_name='Jeu', null=True, on_delete=models.SET_NULL)
    league = models.CharField('Ligue', max_length=20)
    hexcolor = models.CharField('Code couleur Hex', max_length=7, blank=True, default='#000000')

    def __str__(self):
        return self.league

    class Meta:
        verbose_name = 'Ligue'
        verbose_name_plural = 'Ligues'