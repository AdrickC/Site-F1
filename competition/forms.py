from django import forms
from .models import EventRegistration




class UpdateRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        exclude_replacement = kwargs.pop("exclude_replacement", False)
        super().__init__(*args, **kwargs)
        if exclude_replacement:
            self.fields["is_registered"].choices = [
                choice for choice in self.fields["is_registered"].choices if choice[0] != "Remplaçant"
            ]

    class Meta:
        model = EventRegistration
        fields = ('is_registered',)

    def clean(self):
        cleaned_data = super().clean()
        is_registered = cleaned_data.get('is_registered')
        if is_registered == '':
            raise forms.ValidationError("Vous devez choisir une option.")
        return cleaned_data


class UpdateReplacementForm(forms.ModelForm):
    wants_to_replace = forms.BooleanField(label="Je souhaite remplacer")

    class Meta:
        model = EventRegistration
        fields = ('wants_to_replace',)

    def clean(self):
        cleaned_data = super().clean()
        wants_to_replace = cleaned_data.get('wants_to_replace')
        return cleaned_data
    

class CancelReplacementForm(forms.Form):
    confirm_cancellation = forms.BooleanField(
        label="Je souhaite annuler ma participation en tant que remplaçant",
        required=False,
    )


# forms.py



