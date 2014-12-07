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
               
#update profile
class UserFormUpdateProfile(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname','login', 'password')
        widgets = {
            'name' : forms.TextInput(),
            'surname' : forms.TextInput(),
            'login' : forms.EmailInput(),
            'password' : forms.PasswordInput()
    }

def clean_email(self):
    login = self.cleaned_data.get('login')
    password = self.cleaned_data.get('password')

    if login and User.objects.filter(login=login).exclude(password=password).count():
        raise forms.ValidationError('Ten login juz istnieje w bazie!')
    return login

def save(self, commit=True):
    user = super(UserFormSignUp, self).save(commit=False)
    user.login = self.cleaned_data['login']

    if commit:
        user.save()

    return user