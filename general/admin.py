from django.contrib import admin
from .models import Circuit, Team, League, Platform, Game


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    ordering = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'game', 'logo')
    ordering = ('team',)

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league', 'game', 'hexcolor')
    ordering = ('league', 'hexcolor')

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('platform',)
    ordering = ('platform',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)