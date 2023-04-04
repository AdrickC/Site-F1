from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='f1cs-home'),
    path('f1cs-tv/', views.f1cstv, name='f1cs-tv'),
    path('evenements/', include('competition.urls')),
]
