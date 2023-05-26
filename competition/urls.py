from django.urls import path
from . import views


urlpatterns = [
    path('<slug:game_slug>/<int:event_id>/', views.event, name='event'),
    path('<slug:game_slug>/<int:event_id>/resultats', views.event_results, name='event-results'),
    path('<slug:game_slug>/<int:event_id>/entree-resultats', views.submit_event_results, name='submit-event-result'),
    path('<slug:game_slug>/<int:event_id>/maj-inscription/', views.update_registration, name='event-registration'),
    path('<slug:game_slug>/calendrier/', views.game_calendar, name='game-calendar'),
    path('<slug:game_slug>/classement-pilotes/', views.driver_standings, name='driver-standings'),
    path('<slug:game_slug>/classement-constructeurs/', views.constructor_standings, name='constructor-standings'),
]