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
