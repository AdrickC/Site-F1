from django.urls import path
from . import views


urlpatterns = [
    path('reclamation/creer/<int:event_id>/', views.create_claim, name='create-claim'),
    path('reclamation/liste/', views.claim_list, name='claim-list'),
    path('reclamation/detail/<int:claim_id>/', views.claim_detail, name='claim-detail'),
    path('reclamation/detail/<int:claim_id>/decision/', views.update_claim_response, name='update-claim-response'),
]
