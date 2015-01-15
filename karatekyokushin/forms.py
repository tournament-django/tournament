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
     
class KyoEditResultsI(forms.ModelForm):
    class Meta:
        model = Kata
        readonly_fields = ['date','postedTime']
        fields= ('player_id', 'point1I', 'point2I', 'point3I', 'point4I', 'point5I', 'point6I', 'point7I')
        
        CHOICES = (( '', ''), ('1', '1'), ('2', '2'),('3', '3'), ('4', '4'),
                   ('5', '5'), ('6', '6'),('7', '7'), ('8', '8'),
                   ('9', '9'), ('10', '10'))
        widgets = {
            'point1I' : forms.Select(choices=CHOICES),
            'point2I' : forms.Select(choices=CHOICES),
            'point3I' : forms.Select(choices=CHOICES),
            'point4I' : forms.Select(choices=CHOICES),
            'point5I' : forms.Select(choices=CHOICES),
            'point6I' : forms.Select(choices=CHOICES),
            'point7I' : forms.Select(choices=CHOICES)
        }
class KyoEditResultsII(forms.ModelForm):
    class Meta:
        model = Kata
        fields= ('player_id', 'point1II', 'point2II', 'point3II', 'point4II', 'point5II', 'point6II', 'point7II')
        CHOICES = (('', ''), ('1', '1'), ('2', '2'),('3', '3'), ('4', '4'),
                   ('5', '5'), ('6', '6'),('7', '7'), ('8', '8'),
                   ('9', '9'), ('10', '10'))
        widgets = {
            'point1II' : forms.Select(choices=CHOICES),
            'point2II' : forms.Select(choices=CHOICES),
            'point3II' : forms.Select(choices=CHOICES),
            'point4II' : forms.Select(choices=CHOICES),
            'point5II' : forms.Select(choices=CHOICES),
            'point6II' : forms.Select(choices=CHOICES),
            'point7II' : forms.Select(choices=CHOICES)
        }
        
        