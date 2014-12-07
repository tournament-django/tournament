from django import forms
from django.forms.models import ModelForm
from main.models import Player, Tournament, PlayerTournament, Team


class CreateTournamentFormShotokan(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'type', 'coaches' )
        widgets = {
            'start': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'datepicker'}),
            'end': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'datepicker'})
        }


class ChooseTournamentFormShotokan(forms.ModelForm):
    class Meta:
        model = Tournament
        name = forms.CharField()

class CreateTeamFormShotokan(ModelForm):
    class Meta:
        model = Team
        fields = ('name',)