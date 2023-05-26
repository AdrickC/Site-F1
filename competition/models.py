from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django import forms
from general.models import Circuit, League, Game, Team
from users.models import License
from datetime import timedelta
from django.utils import timezone



# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom saison')
    game = models.ForeignKey(Game, verbose_name='Nom du jeu', null=True, on_delete=models.SET_NULL)
    start_date = models.DateField(verbose_name='Date début')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Saison'
        verbose_name_plural = 'Saisons'
        ordering = ['-start_date']

    def driver_ranking(self):
        return License.objects.filter(eventresult__event__season=self).annotate(
            total_points=Sum('eventresult__points')
        ).order_by('-total_points')
    
    def constructor_ranking(self):
        return Team.objects.filter(license__eventresult__event__season=self).annotate(
            total_points=Sum('license__eventresult__points')
        ).order_by('-total_points')


class WeekEndFormat(models.Model):
    name = models.CharField('Nom du format', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Format de week-end'
        verbose_name_plural = 'Formats de week-end'


# Course
class Event(models.Model):
    game = models.ForeignKey(Game, verbose_name='Nom du jeu', null=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(Season, verbose_name='Saison', on_delete=models.CASCADE)
    league = models.ForeignKey(League, verbose_name='Ligue', null=True, blank=True, on_delete=models.SET_NULL)
    circuit = models.ForeignKey(Circuit, verbose_name='Circuit', null=True, on_delete=models.SET_NULL)
    event_date = models.DateTimeField(verbose_name="Date de la course")
    weekend_format = models.ManyToManyField(WeekEndFormat, verbose_name="Format du week-end")

    def limit_date(self):
        return self.event_date - timedelta(hours=5.5)
    
    def end_claim(self):
        # Find the first Tuesday after the event_date
        tuesday = self.event_date
        while tuesday.weekday() != 1:
            tuesday += timedelta(days=1)

        # Set the time to 20:00:00
        tuesday_20 = tuesday.replace(hour=20, minute=0, second=0, microsecond=0)
        return tuesday_20

    def claim_period(self):
        return timezone.now() > self.event_date + timedelta(hours=2.5) and timezone.now() < self.end_claim()

    def limit_date_past(self):
        return timezone.now() > self.event_date - timedelta(hours=5.5)

    def time_before_event(self):
        return (self.event_date - timezone.now()).days
    
    @property
    def time_remaining(self):
        delta = self.event_date - timezone.now()
        if delta.days >= 1:
            return delta.days, "jours"
        else:
            hours = delta.total_seconds() // 3600
            return int(hours), "heures"
        
    def days_before_event(self):
        delta = self.event_date - timezone.now()
        if delta.days > 0:
            return delta.days
        return 0

    def hours_remaining_today(self):
        delta = self.event_date - timezone.now()
        if delta.days == 0:
            hours = delta.total_seconds() // 3600
            return int(hours)
        return None
    
    def is_event_in_progress(self):
        now = timezone.now()
        event_start = self.event_date
        event_end = self.event_date + timedelta(hours=2, minutes=30)
        return event_start <= now <= event_end
    
    def is_event_over(self):
        now = timezone.now()
        event_end = self.event_date + timedelta(hours=2, minutes=30)
        return now > event_end



    def __str__(self):
        return str(self.league) + ' - ' + str(self.circuit) + ' - ' + str(self.season)
    
    

    class Meta:
        verbose_name = 'Course championnat'
        verbose_name_plural = 'Courses championnats'
        ordering = ['event_date']




is_registered_choices = (
    ('Absent', 'Absent'),
    ('Présent', 'Présent'),
    ('Remplaçant', 'Remplaçant'),
)

class EventRegistration(models.Model):
    license = models.ForeignKey(License, verbose_name='Licence', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name='Equipe', null=True, blank=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, verbose_name='Evénement', on_delete=models.CASCADE)
    is_registered = models.CharField(verbose_name="Présence", max_length=50, default='En attente', choices=is_registered_choices)
    registration_date = models.DateTimeField(verbose_name="Date de l'inscription", null=True)

    def __str__(self):
        return str(self.license)

    class Meta:
        verbose_name = 'Inscription course'
        verbose_name_plural = 'Inscriptions course'


class EventResult(models.Model):
    event = models.ForeignKey(Event, verbose_name="Événement", on_delete=models.CASCADE)
    phase = models.ForeignKey(WeekEndFormat, verbose_name="Épreuve", on_delete=models.CASCADE)
    license = models.ForeignKey(License, verbose_name='Licence', on_delete=models.CASCADE)
    is_substitute = models.BooleanField(default=False)
    position = models.PositiveIntegerField(verbose_name="Position", null=True)
    points = models.PositiveIntegerField(verbose_name="Points", default=0, blank=True, editable=False)
    best_lap = models.BooleanField(verbose_name="Meilleur tour en course", default=False)

    class Meta:
        verbose_name = 'Résultat événement'
        verbose_name_plural = 'Résultats événement'
        unique_together = ['event', 'phase', 'license']

    def __str__(self):
        return f"Événement {self.event} - Épreuve {self.phase} - Licence {self.license}"

    def save(self, *args, **kwargs):
        scoring_rule = ScoringRule.objects.filter(
            season=self.event.season, 
            weekend_format=self.phase,
            position=self.position
        ).first()

        if scoring_rule:
            self.points = scoring_rule.points
            if self.best_lap:
                self.points += scoring_rule.best_lap
        else:
            self.points = 0

        super().save(*args, **kwargs)
        


class ScoringRule(models.Model):
    season = models.ForeignKey(Season, verbose_name="Saison", default=1, on_delete=models.CASCADE)
    weekend_format = models.ForeignKey(WeekEndFormat, verbose_name="Epreuve", default=1, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(verbose_name="Position")
    points = models.PositiveIntegerField(verbose_name="Points")
    best_lap = models.PositiveIntegerField(verbose_name="Points pour meilleur tour", default=0)

    class Meta:
        unique_together = ['season', 'weekend_format', 'position']
        ordering = ['season', 'weekend_format', 'position']
        verbose_name = 'Règle de calcul de points'
        verbose_name_plural = 'Règles de calcul de points'

    def __str__(self):
        return f"Saison {self.season} - Format {self.weekend_format.name} - Position {self.position}: {self.points} points"


