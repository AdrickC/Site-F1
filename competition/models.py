from django.db import models
from django.urls import reverse
from django import forms
from general.models import Circuit, League, Game
from datetime import timedelta
from django.utils import timezone
from users.models import License



# Create your models here.


class Season(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom saison')
    start_date = models.DateField(verbose_name='Date début')
    end_date = models.DateField(verbose_name='Date fin')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Saison'
        verbose_name_plural = 'Saisons'
        ordering = ['-start_date']


# Course
class Event(models.Model):
    game = models.ForeignKey(Game, verbose_name='Nom du jeu', null=True, on_delete=models.SET_NULL)
    season = models.ForeignKey(Season, verbose_name='Saison', on_delete=models.CASCADE)
    league = models.ForeignKey(League, verbose_name='Ligue', null=True, on_delete=models.SET_NULL)
    circuit = models.ForeignKey(Circuit, verbose_name='Circuit', null=True, on_delete=models.SET_NULL)
    event_date = models.DateTimeField(verbose_name="Date de la course")

    #def save(self, *args, **kwargs):
        #if self.league not in League.objects.filter(game=self.game):
            #raise forms.ValidationError(f"You cannot use {self.league} for {self.game}")
        #super().save(*args, **kwargs)

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
    event = models.ForeignKey(Event, verbose_name='Evénement', on_delete=models.CASCADE)
    is_registered = models.CharField(verbose_name="S'est enregistré", max_length=50, default='En attente', choices=is_registered_choices)
    registration_date = models.DateTimeField(verbose_name="Date de l'inscription", null=True)

    def __str__(self):
        return str(self.license)

    class Meta:
        verbose_name = 'Inscription course'
        verbose_name_plural = 'Inscriptions course'




