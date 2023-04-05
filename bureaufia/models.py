from django.db import models


# Create your models here.



class ClaimRegistration(models.Model):
    license = models.ForeignKey('users.License', verbose_name='Licence', on_delete=models.CASCADE)
    event_registration = models.ForeignKey('competition.EventRegistration', verbose_name="Participant réclamé", on_delete=models.CASCADE)
    session_type_choices = (
        ('Qualifications', 'Qualifications'),
        ('Course', 'Course'),
    )
    session_type = models.CharField(verbose_name="Type de session", max_length=50, choices=session_type_choices)
    lap_number = models.PositiveIntegerField(verbose_name="Tour de l'incident")
    incident_description = models.TextField(verbose_name="Description de l'incident")
    video_url = models.URLField(verbose_name="URL de la vidéo")
    video_timestamp = models.CharField(verbose_name="Timecode de l'incident", max_length=15)
    admin_response = models.TextField(verbose_name="Réponse de l'administrateur", null=True, blank=True)
    is_resolved = models.BooleanField(verbose_name='Réclamation traitée', default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Réclamation championnat'
        verbose_name_plural = 'Réclamations championnat'



# models.py
class EventResult(models.Model):
    event = models.ForeignKey('competition.Event', verbose_name="Evénement", on_delete=models.CASCADE)
    season = models.ForeignKey('competition.Season', verbose_name="Saison", on_delete=models.CASCADE)
    license = models.ForeignKey('users.License', verbose_name="Licence", on_delete=models.CASCADE)
    position = models.PositiveIntegerField(verbose_name="Position")
    best_lap = models.BooleanField(verbose_name="Meilleur tour en course", default=False)
    points = models.PositiveIntegerField(verbose_name="Points")

    class Meta:
        unique_together = ('event', 'license')
        ordering = ['position']

    def __str__(self):
        return f'{self.event} - {self.license} - Position: {self.position} - Points: {self.points}'
    
    class Meta:
        verbose_name = 'Résultat course'
        verbose_name_plural = 'Résultats course'

    @classmethod
    def calculate_driver_standings(cls, season=None):
        from users.models import License
        drivers = License.objects.all()
        driver_standings = []

        for driver in drivers:
            if season:
                points = cls.objects.filter(license=driver, season=season).aggregate(total_points=models.Sum('points'))['total_points'] or 0
            else:
                points = cls.objects.filter(license=driver).aggregate(total_points=models.Sum('points'))['total_points'] or 0
            driver_standings.append((driver, points))

        driver_standings.sort(key=lambda x: x[1], reverse=True)
        return driver_standings

    @classmethod
    def calculate_constructor_standings(cls, season=None):
        from general.models import Team
        from users.models import License
        teams = Team.objects.all()
        constructor_standings = []

        for team in teams:
            team_members = License.objects.filter(team=team)
            if season:
                points = cls.objects.filter(license__in=team_members, season=season).aggregate(total_points=models.Sum('points'))['total_points'] or 0
            else:
                points = cls.objects.filter(license__in=team_members).aggregate(total_points=models.Sum('points'))['total_points'] or 0
            constructor_standings.append((team, points))

        constructor_standings.sort(key=lambda x: x[1], reverse=True)
        return constructor_standings
