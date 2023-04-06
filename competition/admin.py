from django.contrib import admin
from .models import Event, EventRegistration, Season


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'league', 'game', 'season', 'event_date',)
    ordering = ('-event_date',)


#@admin.register(SpecialEvent)
#class SpecialEventAdmin(admin.ModelAdmin):
    #list_display = ('game', 'circuit', 'event_date',)
    #ordering = ('-event_date',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('license', 'event', 'is_registered', 'registration_date',)
    ordering = ('-registration_date',)


#@admin.register(SpecialEventRegistration)
#class SpecialEventRegistrationAdmin(admin.ModelAdmin):
    #list_display = ('license', 'event', 'is_registered', 'registration_date',)
    #ordering = ('-registration_date',)



@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'start_date')
    ordering = ('-start_date',)
    