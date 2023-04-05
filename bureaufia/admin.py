from django.contrib import admin
from bureaufia.models import ClaimRegistration, EventResult

# Register your models here.


@admin.register(ClaimRegistration)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('license', 'event_registration', 'session_type', 'lap_number', 'created_at')


@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    list_display = ('event', 'license', 'position', 'best_lap', 'points')
    ordering = ('event', 'position')