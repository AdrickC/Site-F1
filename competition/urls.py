from django.urls import path
from . import views


urlpatterns = [
    path('<int:event_id>/', views.event, name='event'),
    path('<int:event_id>/maj-inscription/', views.update_registration, name='event-registration'),
    path('calendrier/', views.calendar, name='calendar'),
    path('classement-pilotes/', views.driver_standings, name='driver-standings'),
    path('classement-constructeurs/', views.constructor_standings, name='constructor-standings'),
]