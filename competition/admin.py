from django.contrib import admin
from .models import Event, EventRegistration, Season, ScoringRule, WeekEndFormat, EventResult


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'league', 'game', 'season', 'event_date', 'display_weekend_format',)
    ordering = ('-event_date',)

    def display_weekend_format(self, obj):
        return ", ".join([format.name for format in obj.weekend_format.all()])
    display_weekend_format.short_description = 'Formats du week-end'



#@admin.register(SpecialEvent)
#class SpecialEventAdmin(admin.ModelAdmin):
    #list_display = ('game', 'circuit', 'event_date',)
    #ordering = ('-event_date',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('license', 'team', 'event', 'is_registered', 'registration_date',)
    ordering = ('-registration_date',)


#@admin.register(SpecialEventRegistration)
#class SpecialEventRegistrationAdmin(admin.ModelAdmin):
    #list_display = ('license', 'event', 'is_registered', 'registration_date',)
    #ordering = ('-registration_date',)

class ScoringRuleInline(admin.TabularInline):
    model = ScoringRule
    extra = 10  # nombre de lignes à afficher

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'start_date')
    ordering = ('-start_date',)
    inlines = [ScoringRuleInline]

@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    list_display = ('event', 'phase', 'license', 'position', 'points', 'best_lap',)
    ordering = ('event', 'phase', 'license', 'position',)

    
@admin.register(WeekEndFormat)
class WeekEndFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
"""
@admin.register(ScoringRule)
class ScoringRuleAdmin(admin.ModelAdmin):
    list_display = ('season', 'weekend_format', 'position', 'points', 'best_lap',)
    ordering = ('-season', 'weekend_format', 'position',)
"""