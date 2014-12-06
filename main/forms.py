from django import forms
from django.forms.models import ModelForm
from main.models import *
from django.core import validators

#class SeasonForm(ModelForm):
#    class Meta:
#        model = Season
#        labels = {
#           'year' : 'Rok',
#        }
#        widgets = {
#            'year' : forms.NumberInput(attrs={'min' : '1990', 'max' : '2100', 'value' : '2014',
#                                              'label' : 'rok'})
#        }
        
class UserFormSignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname','login', 'password')
        widgets={
            'login': forms.EmailInput(),
            'password': forms.PasswordInput()
        }

class UserFormSignIn(ModelForm):
    class Meta:
        model = User
        fields = ('login', 'password')
        widgets={
            'password': forms.PasswordInput()
        }
        
class CreateTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
               
class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields= ('name', 'start', 'end' )
        widgets={
            'start': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'datepicker'}),
            'end': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'datepicker'})
        }

class SelectArtsTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields= ('type',)