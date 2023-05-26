from django.contrib import admin
from bureaufia.models import ClaimRegistration

# Register your models here.


@admin.register(ClaimRegistration)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('license', 'event_registration', 'session_type', 'lap_number', 'created_at')

