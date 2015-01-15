from django.db import models

from main.models import *

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    tournament_id = models.ForeignKey(Tournament, null = True)
    playerT_id = models.ManyToManyField(PlayerTournament, blank=True)
    
    KATA = 'KT'
    KUMITE = 'KM'
    TYPE_CHOICES = (
        (KATA, 'kata'),
        (KUMITE, 'kumite')
    )
    type = models.CharField(max_length=3,
                                      choices=TYPE_CHOICES,
                                      default=None)
     
    def __unicode__(self):
        return self.name

class FirstPlayer(models.Model):
    player = models.ForeignKey(Player)

    def __unicode__(self):
        return str(self.player)

class SecondPlayer(models.Model):
    player = models.ForeignKey(Player)
    
    def __unicode__(self):
        return str(self.player)
    
class Fight(models.Model):
    category_id = models.ForeignKey(Category)
    firstplayer = models.ForeignKey(FirstPlayer)
    secondplayer = models.ForeignKey(SecondPlayer, null=True)
    winner = models.IntegerField(null=True)
    TYPE_CHOICES2 = (
        ('knock', 'knockout'),
        ('walko', 'walkover'),
        ('arbit', 'arbiters'),
        ('wazar', 'wazari')
    )
    reason = models.CharField(max_length=5,
                                      choices=TYPE_CHOICES2,
                                      default='arbiters')
    arbitersfor = models.IntegerField(null=True)
    arbitersagainst = models.IntegerField(null=True)
    arbitersdraw = models.IntegerField(null=True)
    round = models.IntegerField()

    def __unicode__(self):
        return str(self.category_id) + " " + str(self.firstplayer) + " " + str(self.secondplayer) 
    
class Kata(models.Model):
    category_id = models.ForeignKey(Category)
    player_id = models.ForeignKey(Player)
    point1I = models.IntegerField(blank=True, null = True)
    point2I = models.IntegerField(blank=True, null = True)
    point3I = models.IntegerField(blank=True, null = True)
    point4I = models.IntegerField(blank=True, null = True)
    point5I = models.IntegerField(blank=True, null = True)
    point6I = models.IntegerField(blank=True, null = True)
    point7I = models.IntegerField(blank=True, null = True)
    resultI = models.IntegerField(blank=True, null = True)
     
    point1II = models.IntegerField(blank=True, null = True)
    point2II = models.IntegerField(blank=True, null = True)
    point3II = models.IntegerField(blank=True, null = True)
    point4II = models.IntegerField(blank=True, null = True)
    point5II = models.IntegerField(blank=True, null = True)
    point6II = models.IntegerField(blank=True, null = True)
    point7II = models.IntegerField(blank=True, null = True)
    resultII = models.IntegerField(blank=True, null = True)
    

    def __unicode__(self):
        return str(self.player_id) + " " + str(self.category_id)