from django.db import models


class User(models.Model):
    login = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name + " " + self.surname


class Coach(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name + " " + self.surname


class Team(models.Model):
    name = models.CharField(max_length=32)
    coach = models.ForeignKey(Coach, null=True)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    team_id = models.ForeignKey(Team, null=True)
    acceptedbycoachteam = models.BooleanField()
    acceptedbyplayer = models.BooleanField()

    def __unicode__(self):
        return self.name + " " + self.surname


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    KYOKUSHIN = 'KYO'
    SHOTOKAN = 'SHO'
    TYPE_CHOICES = (
        (KYOKUSHIN, 'kyokushin'),
        (SHOTOKAN, 'shotokan')
    )
    type = models.CharField(max_length=3,
                            choices=TYPE_CHOICES,
                            default=None,
                            null=True)
    coaches = models.ManyToManyField(Coach, verbose_name="lista trenerow", blank=True)

    def __unicode__(self):
        return unicode(self.name + " " + self.start.strftime('%Y-%m-%d') + " " + self.end.strftime('%Y-%m-%d'))


class PlayerTournament(models.Model):
    player_id = models.ForeignKey(Player)
    tournament_id = models.ForeignKey(Tournament) 
    acceptedbymanager = models.BooleanField()
    acceptedbycoach = models.BooleanField()

    def __unicode__(self):
        return self.player_id


class Manager(models.Model):
    user_id = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament)
