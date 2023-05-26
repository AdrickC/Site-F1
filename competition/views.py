from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile, License
from django.contrib import messages
from competition.models import Event, EventRegistration
from .forms import UpdateRegistrationForm, UpdateReplacementForm, CancelReplacementForm, EventResultForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Case, When, F, Sum, IntegerField
from competition.models import Event, Season, EventRegistration, EventResult
from general.models import League, Game, Team
from django.db.models import Q


def is_admin(user):
    return user.is_staff or user.is_superuser

# Create your views here.

def event(request, game_slug, event_id):

    game = get_object_or_404(Game, slug=game_slug)
    event = Event.objects.get(id=event_id)
    #drivers = Licence.objects.all().order_by('-team')
    registrations = EventRegistration.objects.filter(event= event_id)

    context = {
        'title': str(event.league) + ' ' + str(event.circuit),
        'event': event,
        'registrations': registrations,
    }

    return render(request, 'competition/event.html', context=context)


@login_required
def update_registration(request, game_slug, event_id):
    game = get_object_or_404(Game, slug=game_slug)
    event = Event.objects.get(id=event_id)
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
        return redirect('event', game_slug=game.slug, event_id=event_id)


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
                    return redirect('event', game_slug=game.slug, event_id=event_id)
            else:
                event_registration.is_registered = 'Remplaçant' if form.cleaned_data['wants_to_replace'] else 'Absent'
                event_registration.registration_date = timezone.now()
                event_registration.save()

            messages.success(request, "Ton inscription a été mise à jour avec succès.")
            return redirect('event', game_slug=game.slug, event_id=event_id)
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
def driver_standings(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    season_id = request.GET.get('season', None)
    if season_id:
        selected_season = get_object_or_404(Season, id=season_id)
    else:
        selected_season = Season.objects.filter(game=game).latest('start_date')
    # Affiche l'objet season sélectionné
    standings_by_game = {}
    standings_by_league = {}
    for league in League.objects.filter(game=game):
        standings = License.objects.filter(
            eventresult__event__league=league,
            eventresult__event__season=selected_season
        ).exclude(
            eventresult__is_substitute=True  # Exclude substitutes
        ).annotate(
            league_total_points=Sum('eventresult__points')
        ).order_by('-league_total_points', 'profile__user__last_name', 'profile__user__first_name')

        standings_by_league[league] = standings

    standings_by_game[game] = standings_by_league

    seasons = Season.objects.filter(game=game).order_by('-start_date')
    context = {'game': game, 'standings_by_game': standings_by_game, 'selected_season': selected_season, 'seasons': seasons}
    return render(request, 'competition/driver-standings.html', context)



@login_required
def constructor_standings(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    season_id = request.GET.get('season', None)
    if season_id:
        selected_season = get_object_or_404(Season, id=season_id)
    else:
        selected_season = Season.objects.filter(game=game).latest('start_date')

    standings = Team.objects.filter(
        Q(license__eventresult__event__game=game),
        license__eventresult__event__season=selected_season
    ).annotate(
        total_points=Sum('license__eventresult__points')
    ).order_by('-total_points')

    seasons = Season.objects.filter(game=game).order_by('-start_date')

    context = {'game': game, 'standings': standings, 'selected_season': selected_season, 'seasons': seasons}

    return render(request, 'competition/constructor-standings.html', context)



from django.shortcuts import render, get_object_or_404
from .models import Game, Season, League, Event


def game_calendar(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)

    season_id = request.GET.get('season', None)
    league_id = request.GET.get('league', None)

    if season_id == '':
        selected_season = None
    elif season_id is not None:
        selected_season = get_object_or_404(Season, id=season_id)
    else:
        try:
            selected_season = Season.objects.filter(game=game).latest('start_date')
        except Season.DoesNotExist:
            selected_season = None

    if league_id:
        selected_league = get_object_or_404(League, id=league_id)
    else:
        selected_league = None

    game_events = game.event_set.all()
    if selected_season:
        game_events = game_events.filter(season=selected_season)
    if selected_league:
        game_events = game_events.filter(league=selected_league)

    events_by_game = {game: game_events}

    seasons = Season.objects.filter(game=game).order_by('-start_date')
    leagues = League.objects.filter(game=game).order_by('league')

    context = {
        'title': f'Calendrier - {game.name}',
        'events_by_game': events_by_game,
        'selected_season': selected_season,
        'selected_league': selected_league,
        'seasons': seasons,
        'leagues': leagues,
    }
    return render(request, 'competition/calendar.html', context)



from django.shortcuts import get_object_or_404, render
from collections import defaultdict
from .models import Event, EventResult

def event_results(request, game_slug, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Fetch all results for this event
    results = EventResult.objects.filter(event=event).order_by('phase', 'position')

    # Organize results by phase
    event_results = defaultdict(list)
    for result in results:
        event_results[result.phase].append(result)

    context = {
        'event': event,
        'event_results': dict(event_results),  # convert back to regular dict for template
    }

    return render(request, 'competition/event-results.html', context)




from django.forms import modelformset_factory

@login_required
@user_passes_test(is_admin)
def submit_event_results(request, game_slug, event_id):
    game = get_object_or_404(Game, slug=game_slug)
    event = Event.objects.get(id=event_id)
    EventResultFormSet = modelformset_factory(EventResult, form=EventResultForm, extra=0)

    if not event.is_event_over():
        messages.warning(request, "Il ne sera possible de rentrer les résultats qu'à la fin de l'événement.")
        return redirect('event', game_slug=game.slug, event_id=event_id)

    if request.method == 'POST':
        formsets = []
        for phase in event.weekend_format.all():
            prefix = f'phase_{phase.id}'
            formset = EventResultFormSet(request.POST, prefix=prefix, form_kwargs={'event': event}, queryset=EventResult.objects.filter(event=event, phase=phase))
            formsets.append((phase, formset))

        if all(formset.is_valid() for _, formset in formsets):
            all_positions_unique = True
            all_best_lap_unique = True
            for _, formset in formsets:
                positions = [form.cleaned_data['position'] for form in formset]
                best_laps = [form.cleaned_data['best_lap'] for form in formset]
                if len(positions) != len(set(positions)):  # Check uniqueness of positions within each event
                    all_positions_unique = False
                if best_laps.count(True) > 1:  # Check uniqueness of best lap within each event
                    all_best_lap_unique = False

            if not all_positions_unique:
                messages.warning(request, "Les positions doivent être uniques pour chaque épreuve.")
            elif not all_best_lap_unique:
                messages.warning(request, "Il ne peut y avoir qu'un seul meilleur tour par épreuve.")
            else:  # No break, all formsets are valid and positions are unique
                for _, formset in formsets:
                    instances = formset.save(commit=False)  # Don't save directly
                    for instance in instances:
                        instance.save()  # This will call the custom save() method
                messages.success(request, "Votre saisie a été soumise avec succès.")

        #else:
            #for _, formset in formsets:
                #if not formset.is_valid():
                    #messages.error(request, f'Erreur de validation : {formset.errors}')

    else:
        formsets = []
        for phase in event.weekend_format.all():
            prefix = f'phase_{phase.id}'
            event_results = EventResult.objects.filter(event=event, phase=phase)
            if not event_results.exists():
                registered_licenses = EventRegistration.objects.filter(event=event).values_list('license', flat=True)
                substitute_licenses = EventRegistration.objects.filter(event=event, is_registered='Remplaçant', team__isnull=False).values_list('license', flat=True)
                all_licenses = list(set(registered_licenses) | set(substitute_licenses))
                for license in all_licenses:
                    team = EventRegistration.objects.get(event=event, license_id=license).team
                    if team:  # Check if team is not empty
                        EventResult.objects.create(event=event, phase=phase, license_id=license)
                event_results = EventResult.objects.filter(event=event, phase=phase)
            formset = EventResultFormSet(prefix=prefix, queryset=event_results)
            formsets.append((phase, formset))

    context = {
        'formsets': formsets,
        'event': event,
    }

    return render(request, 'competition/submit-event-result.html', context)








#@login_required
#def registration(request, event_id):
    #event = Event.objects.get(id= event_id)
    #return render(request, 'competition/event.html', {'title': event, 'event': event})