from django import forms
from django.forms.models import ModelForm
from main.models import *
from karatekyokushin.models import *
from django.core import validators
from django.utils import dateformat

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
        

class KyoCreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ('name', 'type',)
     
