from django.shortcuts import render, redirect, get_object_or_404
from users.models import Profile
from django.contrib import messages
from competition.models import Event, Season, EventRegistration, EventResult
from .forms import ClaimForm, EventResultForm
from .models import ClaimRegistration
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.decorators import user_passes_test
from general.models import League, Game
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from users.models import License


# Create your views here.

def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def create_claim(request, event_id):
    event = Event.objects.get(id=event_id)
    profile = Profile.objects.get(user=request.user)
    license = License.objects.get(profile=profile)

    # Récupérer les inscriptions à l'événement
    event_registrations = EventRegistration.objects.filter(event=event)

    # Vérifier si l'utilisateur actuel a participé
    user_participated = event_registrations.filter(license=license).exists()

    # Si l'utilisateur n'a pas participé, retournez une réponse 403 Forbidden ou redirigez vers une autre page
    if not user_participated:
        messages.warning(request, "Vous ne pouvez pas accéder à cette page car vous n'avez pas participé à cet événement.")
        return redirect('event', event_id=event_id)

    if not event.claim_period():
        messages.warning(request, "La période de réclamation est terminée.")
        return redirect('event', event_id=event_id)

    if request.method == 'POST':
        form = ClaimForm(request.POST, event_id=event_id)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.license = license
            claim.save()
            messages.success(request, "Votre réclamation a été soumise avec succès.")
            return redirect('event', event_id=event_id)
    else:
        form = ClaimForm(event_id=event_id)

    context = {
        'form': form,
        'event': event,
    }

    return render(request, 'bureaufia/claim-form.html', context=context)


@login_required
def claim_detail(request, claim_id):
    claim = get_object_or_404(ClaimRegistration, id=claim_id)
    context = {
        'claim': claim,
    }
    return render(request, 'bureaufia/claim-detail.html', context=context)


@login_required
@user_passes_test(is_admin)
def update_claim_response(request, claim_id):
    claim = get_object_or_404(ClaimRegistration, id=claim_id)

    if request.method == 'POST':
        admin_response = request.POST.get('admin_response', '').strip()
        points_removed = int(request.POST.get('points_removed', 0))

        if admin_response:
            claim.admin_response = admin_response
            claim.is_resolved = True
        else:
            claim.admin_response = admin_response
            claim.is_resolved = False
        claim.save()

        #license = claim.event_registration.license
        #license.license_points -= points_removed
        #license.save()

        messages.success(request, "Votre saisie a été mise à jour avec succès.")

    return redirect('claim-detail', claim_id=claim_id)


@login_required
def claim_list(request):
    league_id = request.GET.get('league', '')
    season_id = request.GET.get('season', '')

    claims = ClaimRegistration.objects.select_related(
        'license__profile__user',
        'event_registration__license__profile__user',
        'event_registration__event__circuit',
        'event_registration__event__league',
    ).order_by('-event_registration__event__event_date', '-created_at')

    if not request.user.is_staff and not request.user.is_superuser:
        claims = claims.filter(is_resolved=True)

    if league_id:
        claims = claims.filter(event_registration__event__league_id=league_id)

    if season_id:
        claims = claims.filter(event_registration__event__season_id=season_id)

    claims = claims.all()

    leagues = League.objects.all()
    seasons = Season.objects.all()

    claims_per_page = 10 
    page = request.GET.get('page', 1)

    paginator = Paginator(claims, claims_per_page)
    try:
        claims = paginator.page(page)
    except PageNotAnInteger:
        claims = paginator.page(1)
    except EmptyPage:
        claims = paginator.page(paginator.num_pages)
        
    context = {
        'claims': claims,
        'leagues': leagues,
        'seasons': seasons,
        'league_id': league_id,
        'season_id': season_id,
    }
    return render(request, 'bureaufia/claim-list.html', context=context)


