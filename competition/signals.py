from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from .models import Event, EventRegistration
from users.models import License



@receiver(post_save, sender=Event)
def create_event_registrations(sender, instance, created, **kwargs):
    if created:
        # Filtrer les licences en fonction de la ligue de l'événement
        licenses = License.objects.filter(leagues=instance.league)

        registrations = [EventRegistration(license=license, team=license.team, event=instance) for license in licenses]

        with transaction.atomic():
            EventRegistration.objects.bulk_create(registrations)

