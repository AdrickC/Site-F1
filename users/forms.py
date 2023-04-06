from django import forms
from django.forms import FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, License

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom")
    email = forms.EmailField(label="Adresse mail")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse mail")

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='Photo de profil', widget=FileInput)

    class Meta:
        model = Profile
        fields = ['image']



from django import forms
from .models import ChampionshipApplication, Team

class ChampionshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ChampionshipApplication
        fields = ['first_name', 'platform', 'platform_id', 'availability', 'teammates', 'preferred_team1', 'preferred_team2', 'preferred_team3']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.TextInput(attrs={'class': 'form-control'}),
            'platform_id': forms.TextInput(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
            'teammates': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_team1': forms.Select(attrs={'class': 'form-control'}),
            'preferred_team2': forms.Select(attrs={'class': 'form-control'}),
            'preferred_team3': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Prénom',
            'platform': 'Sur quelle plateforme jouez-vous à F1 ?',
            'platform_id': 'SteamID, OriginID, ... (en fonction de votre réponse précédente)',
            'availability': 'Disponibilités',
            'teammates': 'Coéquipiers souhaités',
            'preferred_team1': 'Ecurie 1 souhaitée',
            'preferred_team2': 'Ecurie 2 souhaitée',
            'preferred_team3': 'Ecurie 3 souhaitée',
        }  


