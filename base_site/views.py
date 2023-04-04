from django.contrib import messages
from django.shortcuts import redirect, render
from general.models import Game



def base(request):
    return render(request, 'base_site/base.html')



def home(request):
    games = Game.objects.all()
    return render(request, 'base_site/home.html', context={'title': 'Accueil', 'games': games})



def f1cstv(request):
    return render(request, 'base_site/f1cs-tv.html', {'title': 'F1CS TV'})