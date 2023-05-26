from django import forms
from .models import ClaimRegistration
from competition.models import EventRegistration, EventResult
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from users.models import License


class ClaimForm(forms.ModelForm):
    class Meta:
        model = ClaimRegistration
        fields = ('event_registration', 'session_type', 'lap_number', 'incident_description', 'video_url', 'video_timestamp')

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id', None)
        super().__init__(*args, **kwargs)

        if event_id:
            registrations = EventRegistration.objects.filter(event_id=event_id).select_related('license')
            self.fields['event_registration'].queryset = registrations

        self.fields['incident_description'].widget.attrs.update({'rows': 5})




class EventResultForm(forms.ModelForm):
    class Meta:
        model = EventResult
        fields = ('license', 'position', 'best_lap')

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super(EventResultForm, self).__init__(*args, **kwargs)
        if self.event:
            self.fields['license'].queryset = License.objects.filter(eventregistration__event=self.event)


    
