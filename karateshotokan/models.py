from django.db import models

from main.models import Player, Tournament, PlayerTournament, User

# Create your models here.

class Document(models.Model):
    file = models.FileField(upload_to='media/regulaminy/%Y/%m/%d')

class CategoryShotokan(models.Model):
    name = models.CharField(max_length=50)
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

class PlayerAka(models.Model):
    player = models.ForeignKey(Player)

class PlayerAo(models.Model):
    player = models.ForeignKey(Player)

class FightShotokan(models.Model):
    category_id = models.ForeignKey(CategoryShotokan)
    aka = models.ForeignKey(PlayerAka)
    ao = models.ForeignKey(PlayerAo, null=True)
    winner = models.IntegerField(null=True)
    TYPE_CHOICES2 = (
        ('shika', 'shikaku'),
        ('hanso', 'hansoku')
    )
    reason = models.CharField(max_length=5,
                                      choices=TYPE_CHOICES2,
                                      default='arbiters')
    arbitersfor = models.IntegerField(null=True)
    arbitersagainst = models.IntegerField(null=True)
    round = models.IntegerField()
