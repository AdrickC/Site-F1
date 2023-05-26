from django.contrib import admin
from .models import Profile, License, ChampionshipApplication

@admin.register(Profile)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user',)
    ordering = ('user',)


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('profile', 'leagues_list', 'team', 'status',)
    ordering = ('profile',)

    def leagues_list(self, obj):
        return ", ".join([str(league) for league in obj.leagues.all()])
    leagues_list.short_description = 'Ligues'


@admin.register(ChampionshipApplication)
class ChampionshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'platform', 'availability')
    ordering = ('user',)