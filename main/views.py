from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

from main.forms import *
from karatekyokushin.forms import *

from models import Tournament

# Create your views here.
def home(request):
    tournaments = Tournament.objects.all()

    return render(request, 'home.html', {
        'tournaments': tournaments, 
    })

def signUp(request):
    if request.method == 'POST':
        form = UserFormSignUp(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserFormSignUp()
    return render(request, 'signUp.html', {
        'formset': form,
    })


def signIn(request):
    if request.method == 'POST':
        form = UserFormSignIn(request.POST)
        try:
            us = User.objects.get(login=form.data['login'], password=form.data['password'])
        except:
            return redirect('/signIn')
        request.session.set_expiry(3600) # ustawienie czasu trwania sesji na 1h
        request.session['user'] = us.id
        request.session['login'] = us.login
        return redirect('/user/')
    else:
        form = UserFormSignIn()
        return render_to_response('signIn.html', RequestContext(request, {'formset': form}))


def logout(request):
    del request.session["user"]
    del request.session["login"]
    request.session.modified = True
    return redirect('/')

def user(request):
    if 'user' in request.session:
        template = loader.get_template('user.html')
        user = User.objects.get(id=request.session['user'])
        if Player.objects.filter(user_id=user.id, acceptedbycoachteam=True, acceptedbyplayer=False):
            playerteam = Player.objects.get(user_id=user.id, acceptedbycoachteam = True, acceptedbyplayer=False)
            
        else:
            playerteam = None
        
        if Player.objects.filter(user_id=user.id, acceptedbycoachteam=True, acceptedbyplayer=True):
            player = Player.objects.get(user_id=user.id, acceptedbycoachteam = True, acceptedbyplayer=True)
            playersT = PlayerTournament.objects.filter(player_id=player, acceptedbymanager=True, acceptedbycoach=True)
        else:
            playersT = None
            
        if Coach.objects.filter(user_id=user):
            coach = Coach.objects.get(user_id=user)
            teams = Team.objects.filter(coach = coach)
            coachtournaments = Tournament.objects.filter(coaches=coach)
            AplayersT = list()
            for team in teams:
                playersC = Player.objects.filter(team_id=team)
                for playerC in playersC:
                    if PlayerTournament.objects.filter(player_id=playerC, acceptedbymanager=True, acceptedbycoach=False):
                        AplayersT.append(PlayerTournament.objects.get(player_id=playerC, acceptedbymanager=True, acceptedbycoach=False))
        else:
            teams = None
            coachtournaments = None
            AplayersT = None
        
        if Manager.objects.filter(user_id=user.id):
            managers = Manager.objects.filter(user_id = user.id)
            managertournaments = list()
            EplayersT = list()
            for manager in managers:
                tournament = Tournament.objects.get(id=manager.tournament.id)
                managertournaments.append(tournament)
                for EplayerT in PlayerTournament.objects.filter(tournament_id = tournament, acceptedbymanager=False, acceptedbycoach=True):
                    EplayersT.append(EplayerT)
        else:
            managertournaments = None
            EplayersT = None
        if EplayersT:
            EplayersT.sort(key=lambda player: player.player_id.team_id.name, reverse=False)  
        context = RequestContext(request, {'playersT': playersT, 'ctournaments': coachtournaments, 'mtournaments': managertournaments, 'teams': teams, 'user': user, 'playerteam': playerteam, 'AplayersT': AplayersT, 'EplayersT': EplayersT })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')

#update profile
def updateProfile(request):
    args = {}

    if request.method == 'POST':
        user = User.objects.get(id=request.session['user'])
        form = UserFormUpdateProfile(request.POST, instance=user)
        if form.is_valid():
            inst = form.save()
            request.session['login'] = inst.login
            return redirect('/user/')

    else:
        form = UserFormUpdateProfile()

        args['form'] = form
        return render(request, 'updateProfile.html', args)

def createTeam(request):
    if 'user' in request.session:
        template = loader.get_template('createteam.html')
        
        if request.method == 'POST':
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.session['user'])
                instance=form.save()#instance zawiera zapisany obiekt, takze z jego id
                coachobj, bool= Coach.objects.get_or_create(user_id=user, defaults={'name': user.name, 'surname': user.surname})
                Team.objects.filter(id = instance.id).update(coach = coachobj)
                return redirect('/user/')
        else:
           form = CreateTeamForm()
           
        context = RequestContext(request, {
            'form': form,
        })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')

def team(request, team_id):
    template = loader.get_template('team.html')
    team = Team.objects.get(id=team_id)
    players = Player.objects.filter(team_id = team, acceptedbycoachteam=True, acceptedbyplayer = True)
    context = RequestContext(request, {'team': team, 'players':players, })
    return HttpResponse(template.render(context))

def addPlayers(request, team_id):
    if 'user' in request.session:
        template = loader.get_template('addPlayer.html')
        team = Team.objects.get(id=team_id)
        users = User.objects.all()
        for player in Player.objects.all():
            users = users.exclude(id=player.user_id.id)
        context = RequestContext(request, {'team': team, 'users':users, })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def userToAdd(request, user_id, team_id):
    user = User.objects.get(id=user_id)
    team = Team.objects.get(id=team_id)
    Player.objects.create(user_id=user, name=user.name, surname=user.surname, team_id=team, acceptedbycoachteam=True, acceptedbyplayer = False)
    return redirect('addPlayers', team_id = team.id)

def playerToTeamAccept(request, player_id):
    Player.objects.filter(id=player_id).update(acceptedbyplayer = True)
    return redirect('/user/')

def updateTournament(request, tournament_id):
    if 'user' in request.session:
        template = loader.get_template('updatetournament.html')
        tournament = Tournament.objects.get(id = tournament_id)
        if request.method == 'POST':
            form = CreateTournamentForm(request.POST, instance=tournament)
            if form.is_valid():
                user = User.objects.get(id=request.session['user'])
                form.save()#instance zawiera zapisany obiekt, takze z jego id
                return redirect('tournament', tournament_id = tournament.id)
        else:
           form = CreateTournamentForm()

        context = RequestContext(request, {
            'form': form,
        })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def enterForTournament(request, tournament_id, user_id):
    if 'user' in request.session:
        template = loader.get_template('enterForTournament.html')
        tournament = Tournament.objects.get(id=tournament_id)
        user = User.objects.get(id=user_id)
        if Coach.objects.filter(user_id=user):
            coach = Coach.objects.get(user_id=user)
            players = list()
            teams = list()
            for team in Team.objects.filter(coach = coach):
                teamTrue = False
                playersC = Player.objects.filter(team_id = team, acceptedbycoachteam=True, acceptedbyplayer=True)
                for playerC in playersC:
                    if PlayerTournament.objects.filter(tournament_id=tournament, player_id = playerC).count()==0:
                        players.append(playerC)
                        teamTrue = True
                if teamTrue:
                    teams.append(team)
        context = RequestContext(request, {'tournament': tournament, 'players':players, 'teams':teams })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def enterAllPlayersToTournament(request, tournament_id, user_id):
    tournament = Tournament.objects.get(id=tournament_id)
    user = User.objects.get(id=user_id)
    if Coach.objects.filter(user_id=user):
        coach = Coach.objects.get(user_id=user)
        for team in Team.objects.filter(coach = coach):
            playersC = Player.objects.filter(team_id = team, acceptedbycoachteam=True, acceptedbyplayer=True)
            for playerC in playersC:
                if PlayerTournament.objects.filter(tournament_id=tournament, player_id = playerC).count()==0:
                    PlayerTournament.objects.create(player_id=playerC, tournament_id=tournament, acceptedbymanager=False, acceptedbycoach=True)
    return redirect('/user/')

def enterPlayersTeamTour(request, team_id, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    team = Team.objects.get(id=team_id)
    for player in Player.objects.filter(team_id = team):
        if PlayerTournament.objects.filter(tournament_id=tournament, player_id = player).count()==0:
            PlayerTournament.objects.create(player_id=player, tournament_id=tournament, acceptedbymanager=False, acceptedbycoach=True)
    return redirect('enterForTournament', tournament_id = tournament.id, user_id = team.coach.user_id.id)

def allPlayersTourAcceptByC(request):
    user = User.objects.get(id=request.session['user'])
    if Coach.objects.filter(user_id=user):
        coach = Coach.objects.get(user_id=user)
        teams = Team.objects.filter(coach = coach)
        for team in teams:
            playersC = Player.objects.filter(team_id=team)
            for playerC in playersC:
                for playerT in PlayerTournament.objects.filter(player_id=playerC, acceptedbymanager=True, acceptedbycoach=False):
                    playerT.tournament_id.coaches.add(coach)
                if PlayerTournament.objects.filter(player_id=playerC, acceptedbymanager=True, acceptedbycoach=False):
                    PlayerTournament.objects.filter(player_id=playerC).update(acceptedbymanager=True, acceptedbycoach = True)
    return redirect('/user/')

def allPlayersTourAcceptByM(request):
    user = User.objects.get(id=request.session['user'])
    if Manager.objects.filter(user_id=user.id):
        managers = Manager.objects.filter(user_id = user.id)
        for manager in managers:
            tournament = Tournament.objects.get(id=manager.tournament.id)
            for EplayerT in PlayerTournament.objects.filter(tournament_id = tournament, acceptedbymanager=False, acceptedbycoach=True):
                PlayerTournament.objects.filter(id = EplayerT.id).update(acceptedbymanager=True, acceptedbycoach = True)
                EplayerT.tournament_id.coaches.add(EplayerT.player_id.team_id.coach)
    return redirect('/user/')

def allTeamTourAcceptByM(request, team_id):
    team = Team.objects.get(id=team_id)
    for player in Player.objects.filter(team_id = team):
        if PlayerTournament.objects.filter(player_id=player, acceptedbymanager=False, acceptedbycoach=True):
            PlayerTournament.objects.filter(player_id=player).update(acceptedbymanager=True, acceptedbycoach = True)
    return redirect('/user/')
