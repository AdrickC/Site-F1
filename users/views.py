from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ChampionshipApplicationForm
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import License


# Page de connexion custom
class CustomLoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('f1cs-home')


# Formulaire d'inscription
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Bienenue {username} ! Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    context = {
        'title': 'Inscriptions', 
        'form': form
        }

    return render(request, 'users/register.html', context)


# Connexion requise pour accéder à cette page
@login_required
def profile_update(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Vos informations ont bien été mises à jour.")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Maj Profil'
    }

    return render(request, 'users/profile-update.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'Profil'})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ChampionshipApplication
from .forms import ChampionshipApplicationForm

@login_required
def championship_registration(request):
    user = request.user
    application_exists = ChampionshipApplication.objects.filter(user=user).exists()

    if application_exists:
        messages.warning(request,"Vous avez déjà postulé pour une licence. Vous ne pouvez pas postuler à nouveau.")
        return redirect('f1cs-home')

    if request.method == 'POST':
        form = ChampionshipApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
        
            profile = request.user.profile
            if not hasattr(profile, 'license'):
                License.objects.create(profile=profile, status='En attente', team=None)
            
            return redirect('championship-registration-success')
    else:
        form = ChampionshipApplicationForm()

    context = {'form': form}
    return render(request, 'users/championship-registration.html', context)


@login_required
def success_page(request):
    return render(request, 'users/championship-registration-success.html')



