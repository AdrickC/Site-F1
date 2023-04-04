from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile, License
from django.contrib import messages
from competition.models import Event, EventRegistration
from .forms import UpdateRegistrationForm, UpdateReplacementForm, CancelReplacementForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Case, When, F, Sum, IntegerField
from competition.models import Event, Season, EventRegistration
from bureaufia.models import EventResult
from general.models import League, Game


# Create your views here.

def event(request, event_id):
    
    event = Event.objects.get(id= event_id)
    #drivers = Licence.objects.all().order_by('-team')
    registrations = EventRegistration.objects.filter(event= event_id)

    context = {
        'title': str(event.league) + ' ' + str(event.circuit),
        'event': event,
        'registrations': registrations,
    }

    return render(request, 'competition/event.html', context=context)


@login_required
def update_registration(request, event_id):
    
    event = Event.objects.get(id= event_id)
    profile = Profile.objects.get(user=request.user)
    license = License.objects.get(profile=profile)
    time_left = event.event_date - timezone.now()
    belongs_to_league = event.league in license.leagues.all()

    event_registration = EventRegistration.objects.filter(event=event_id, license__profile=profile).first()
    if not event_registration:
        license = License.objects.get(profile=profile)
        event_registration = EventRegistration.objects.create(license=license, event=event, is_registered='En attente')


    if time_left.total_seconds() <= 19800: # 19800 secondes = 5h30
        messages.warning(request, "La période d'inscription est terminée.")
        return redirect('event', event_id=event_id)


    if request.method == 'POST':
        if belongs_to_league:
            form = UpdateRegistrationForm(request.POST, instance=event_registration)
        else:
            if event_registration.is_registered == 'Remplaçant':
                form = CancelReplacementForm(request.POST)
            else:
                form = UpdateReplacementForm(request.POST, instance=event_registration)

        if form.is_valid():
            if belongs_to_league:
                event_registration.is_registered = form.cleaned_data['is_registered']
                event_registration.registration_date = timezone.now()
                event_registration.save()
            elif isinstance(form, CancelReplacementForm):
                if form.cleaned_data['confirm_cancellation']:
                    event_registration.delete()
                    messages.success(request, "Ta participation en tant que remplaçant a été annulée.")
                    return redirect('event', event_id=event_id)
            else:
                event_registration.is_registered = 'Remplaçant' if form.cleaned_data['wants_to_replace'] else 'Absent'
                event_registration.registration_date = timezone.now()
                event_registration.save()

            messages.success(request, "Ton inscription a été mise à jour avec succès.")
            return redirect('event', event_id=event_id)
    else:
        if belongs_to_league:
            form = UpdateRegistrationForm(instance=event_registration, exclude_replacement=belongs_to_league)
        else:
            if event_registration.is_registered == 'Remplaçant':
                form = CancelReplacementForm()
            else:
                form = UpdateReplacementForm(instance=event_registration)

    context = {
        'form': form,
        'event_registration': event_registration,
        'event': event,
        'belongs_to_league': belongs_to_league,
    }

    return render(request, 'competition/event-registration.html', context=context)



@login_required
def driver_standings(request):
    season_id = request.GET.get('season', None)
    if season_id:
        selected_season = get_object_or_404(Season, id=season_id)
    else:
        selected_season = Season.objects.latest('start_date')

    standings_by_game = {}
    for game in Game.objects.all():
        standings_by_league = {}
        for league in League.objects.filter(game=game):
            standings = License.objects.filter(leagues=league, team__game=game).annotate(
                league_total_points=Sum(
                    Case(
                        When(eventresult__event__league=league, eventresult__event__season=selected_season, then=F('eventresult__points')),
                        default=0,
                        output_field=IntegerField(),
                    )
                )
            ).order_by('-league_total_points', 'profile__user__last_name', 'profile__user__first_name')
            standings_by_league[league] = standings
        standings_by_game[game] = standings_by_league

    seasons = Season.objects.all().order_by('-start_date')
    context = {'standings_by_game': standings_by_game, 'selected_season': selected_season, 'seasons': seasons}
    return render(request, 'competition/driver-standings.html', context)


@login_required
def constructor_standings(request):
    season_id = request.GET.get('season', None)
    if season_id:
        selected_season = get_object_or_404(Season, id=season_id)
    else:
        selected_season = Season.objects.latest('start_date')

    standings = EventResult.calculate_constructor_standings(season=selected_season)
    seasons = Season.objects.all().order_by('-start_date')
    context = {'standings': standings, 'selected_season': selected_season, 'seasons': seasons}
    return render(request, 'competition/constructor-standings.html', context)


from django.shortcuts import render
from .models import Game, Season, League

def calendar(request):
    season_id = request.GET.get('season', None)
    league_id = request.GET.get('league', None)

    if season_id:
        selected_season = get_object_or_404(Season, id=season_id)
    else:
        selected_season = None

    if league_id:
        selected_league = get_object_or_404(League, id=league_id)
    else:
        selected_league = None

    games = Game.objects.all()

    events_by_game = {}
    for game in games:
        game_events = Event.objects.filter(game=game)
        if selected_season:
            game_events = game_events.filter(season=selected_season)
        if selected_league:
            game_events = game_events.filter(league=selected_league)
        events_by_game[game] = game_events

    seasons = Season.objects.all().order_by('-start_date')
    leagues = League.objects.all().order_by('league')

    context = {
        'title': 'Calendrier',
        'events_by_game': events_by_game,
        'selected_season': selected_season,
        'selected_league': selected_league,
        'seasons': seasons,
        'leagues': leagues,
    }
    return render(request, 'competition/calendar.html', context)






#@login_required
#def registration(request, event_id):
    #event = Event.objects.get(id= event_id)
    #return render(request, 'competition/event.html', {'title': event, 'event': event})