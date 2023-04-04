from django.contrib import admin
from .models import Profile, License, ChampionshipApplication

@admin.register(Profile)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user',)
    ordering = ('user',)


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('profile', 'team', 'status',)
    ordering = ('profile',)


@admin.register(ChampionshipApplication)
class ChampionshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'platform', 'availability')
    ordering = ('user',)