from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
import random

from karatekyokushin.forms import *
from main.forms import *
# Create your views here.

def KarateKyokushinMain(request):
    template = loader.get_template('kyokushin-main.html')
#    latest_seasons = Season.objects.order_by('-id')[:10]
#    latest_rounds = Round.objects.order_by('-id')[:10]
#    latest_matchday = Matchday.objects.order_by('-id')[:10]
#    latest_matches = Match.objects.order_by('-id')[:10]
    context = RequestContext(request, {
#       'latest_matches': latest_matches,
#       'latest_seasons': latest_seasons,
#       'latest_rounds': latest_rounds,
#        'latest_matchday': latest_matchday,
    })
    return HttpResponse(template.render(context))

def KarateKyokushinCreate(request):
    
    #    if request.method == 'POST':
    #        form = CreateTournamentForm(request.POST)
    #        if form.is_valid():
    #            form.save()
    #    else:
    #        form = CreateTournamentForm()
    #    return render(request, 'createtournament.html', {
    #        'form': form, 
    #    })
    if 'user' in request.session:
        template = loader.get_template('createtournament.html')
        
        if request.method == 'POST':
            form = CreateTournamentForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.session['user'])
                instance=form.save()#instance zawiera zapisany obiekt, takze z jego id
                Manager.objects.create(user_id=user, tournament = instance)
                return redirect('/user/')
        else:
           form = CreateTournamentForm()
        
    #    latest_seasons = Season.objects.order_by('-id')[:10]
    #    latest_rounds = Round.objects.order_by('-id')[:10]
    #    latest_matchday = Matchday.objects.order_by('-id')[:10]
    #    latest_matches = Match.objects.order_by('-id')[:10]
        context = RequestContext(request, {
            'form': form,
    #       'latest_matches': latest_matches,
    #       'latest_seasons': latest_seasons,
    #       'latest_rounds': latest_rounds,
    #        'latest_matchday': latest_matchday,
        })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def tournamentOrganization(request, tournament_id):
    template = loader.get_template('tournamentOrganization.html')
    tournament = Tournament.objects.get(id=tournament_id)
    manager = Manager.objects.get(tournament=tournament)
    categories = Category.objects.filter(tournament_id = tournament)
    context = RequestContext(request, {'tournament': tournament, 'categories':categories, 'manager':manager })
    return HttpResponse(template.render(context))

def createCategoryKyo(request, tournament_id):
    if 'user' in request.session:
        template = loader.get_template('kyoukushin-createcategory.html')
        
        if request.method == 'POST':
            form = KyoCreateCategoryForm(request.POST)
            if form.is_valid():
                tournament = Tournament.objects.get(id = tournament_id)
                instance=form.save()#instance zawiera zapisany obiekt, takze z jego id
                Category.objects.filter(id = instance.id).update(tournament_id = tournament)
                return redirect('tournamentOrganization', tournament_id = tournament.id)
        else:
           form = KyoCreateCategoryForm()
        context = RequestContext(request, {
            'form': form,
        })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')  

def kyoCategory(request, category_id):
    template = loader.get_template('kyo-category.html')
    category = Category.objects.get(id=category_id)
    manager = Manager.objects.get(tournament=category.tournament_id)
    teams = list()
    players = list()
    playersT = category.playerT_id.all()
    for playerT in playersT:
        player = playerT.player_id
        players.append(player)
        teams.append(Team.objects.get(id=player.team_id.id))
    fights = Fight.objects.filter(category_id = category)
    print fights
    context = RequestContext(request, {'category': category, 'teams': teams, 'players':players, 'manager':manager, 'fights':fights})
    return HttpResponse(template.render(context))

def kyoAddPlayersToCategory(request, category_id):
    if 'user' in request.session:
        template = loader.get_template('kyoAddPlayerToCategory.html')
        category = Category.objects.get(id=category_id)
        playersT = PlayerTournament.objects.filter(tournament_id=category.tournament_id, acceptedbymanager=True, acceptedbycoach=True)
        players = list()
        for playerCat in category.playerT_id.all():
            playersT = playersT.exclude(id=playerCat.player_id.id)
        for playerT in playersT:
            players.append(playerT.player_id)
        context = RequestContext(request, {'category': category, 'players':players })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def kyoPlayerToCategory(request, player_id, category_id):
    category = Category.objects.get(id=category_id)
    player = Player.objects.get(id = player_id)
    playerT = PlayerTournament.objects.get(player_id = player, tournament_id = category.tournament_id)
    category.playerT_id.add(playerT)
    return redirect('kyoAddPlayersToCategory', category_id = category.id)

def kyoDeletePlayerFromCategory(request, player_id, category_id):
    category = Category.objects.get(id=category_id)
    player = Player.objects.get(id = player_id)
    playerT = PlayerTournament.objects.get(player_id = player, tournament_id = category.tournament_id)
    category.playerT_id.remove(playerT)
    return redirect('kyoCategory', category_id = category.id)

def kyoUpdateCategory(request, category_id):
    if 'user' in request.session:
        template = loader.get_template('kyoUpdateCategory.html')
        category = Category.objects.get(id = category_id)
        if request.method == 'POST':
            form = KyoCreateCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()#instance zawiera zapisany obiekt, takze z jego id
                return redirect('kyoCategory', category_id = category.id)
        else:
           form = KyoCreateCategoryForm()

        context = RequestContext(request, {
            'form': form,
        })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')

def kyoRandPlayers(request, tournament_id):
    tournament = Tournament.objects.get(id = tournament_id)
    categories = Category.objects.filter(tournament_id = tournament)
    for category in categories:
        if category.type=="KM" and category.playerT_id.all().count()>0:
            playersT = list(category.playerT_id.all())
            random.shuffle(playersT)
            i = 0
            while i<len(playersT):
                first = FirstPlayer.objects.create(player = playersT[i].player_id)
                i=i+1
                if i<len(playersT):
                    second = SecondPlayer.objects.create(player = playersT[i].player_id)
                else: 
                    second = None
                Fight.objects.create(category_id = category, firstplayer = first, secondplayer = second, round = 0)
                i=i+1
    return redirect('tournament', tournament_id = tournament.id)
