from django.contrib import messages
from django.shortcuts import redirect, render
from general.models import Game



def base(request):
    return render(request, 'base_site/base.html')


def home(request):
    return render(request, 'base_site/home.html')


def f1cstv(request):
    return render(request, 'base_site/f1cs-tv.html', {'title': 'F1CS TV'})