from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('maj/', views.profile_update, name='profile-update'),
    path('change-mdp/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('password-change-done'), template_name='users/password_change.html'), name='password-change'),
    path('change-mdp-complet/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password-change-done'), 
    path('inscription-championnat/', views.championship_registration, name='championship-registration'),
    path('inscription-championnat/success/', views.success_page, name='championship-registration-success'),
]
