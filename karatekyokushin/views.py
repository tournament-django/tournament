from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
import random
import math

from karatekyokushin.forms import *
from main.forms import *
# Create your views here.

def KarateKyokushinMain(request):
    template = loader.get_template('kyokushin-main.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
    
def kyoTournamentOrganization(request, tournament_id):
    template = loader.get_template('kyoTournamentOrganization.html')
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
                return redirect('kyoTournamentOrganization', tournament_id = tournament.id)
        else:
           form = KyoCreateCategoryForm()
        context = RequestContext(request, {
            'form': form,
        })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')  

def kyoCategory(request, category_id, minround):
    template = loader.get_template('kyo-category.html')
    category = Category.objects.get(id=category_id)
    manager = Manager.objects.get(tournament=category.tournament_id)
    teams = list()
    players = list()
    playersT = category.playerT_id.filter(acceptedbymanager=True, acceptedbycoach = True)
    for playerT in playersT:
        player = playerT.player_id
        players.append(player)
        teams.append(Team.objects.get(id=player.team_id.id))
    if Fight.objects.filter(category_id = category):
        if not Fight.objects.filter(category_id = category, round = str(minround)):
            minround = int(minround) - 3
        fights4 = None
        minround2 = int(minround) + 1
        minround3 = int(minround) + 2
        minround4 = int(minround) + 3
        minround5 = int(minround) + 4
        fights1 = list(Fight.objects.filter(category_id = category, round = str(minround)))
        fights1.reverse() 
        fights2 = list(Fight.objects.filter(category_id = category, round = str(minround2)))
        fights2.reverse()
        fights3 = list(Fight.objects.filter(category_id = category, round = str(minround3)))
        fights3.reverse()
        if not Fight.objects.filter(category_id = category, round = str(minround5)):
            fights4 = list(Fight.objects.filter(category_id = category, round = str(minround4)))
            fights4.reverse()
        if fights1[0].round == 0:
            k=2
            while k<=len(playersT):
                k=k*2
            k=k/4
            empty = k-len(fights2)
        else:
            empty = 0    
        context = RequestContext(request, {'category': category, 'teams': teams, 'players':players, 'manager':manager, 'fights1':fights1, 'fights2':fights2, 'fights3':fights3, 'fights4':fights4, 'empty':xrange(empty)})
    elif Kata.objects.filter(category_id = category):
        katasI = list(Kata.objects.filter(category_id = category))
        NotKataII = False
        for kata in katasI:
            playerT = PlayerTournament.objects.get(player_id = kata.player_id)
            if playerT.acceptedbymanager != True or playerT.acceptedbycoach != True:
                katasI.remove(kata)
            else:
                points = list()
                if kata.point1I != None:
                    points.append(int(kata.point1I))
                if kata.point2I != None:
                    points.append(int(kata.point2I))
                if kata.point3I != None:
                    points.append(int(kata.point3I))
                if kata.point4I != None:
                    points.append(int(kata.point4I))
                if kata.point5I != None:
                    points.append(int(kata.point5I))
                if kata.point6I != None:
                    points.append(int(kata.point6I))
                if kata.point7I != None:
                    points.append(int(kata.point7I))
                points.sort()
                if len(points)>2:
                    points.remove(points[0])
                    points.pop()
                    result = 0
                    for point in points:
                        result = result + point
                    kata.resultI = result
                    Kata.objects.filter(id = kata.id).update(resultI = result)
                else:
                    Kata.objects.filter(id = kata.id).update(resultI = None)
            if playerT.acceptedbymanager == True and playerT.acceptedbycoach == True and kata.resultI == None:
                NotKataII = True
            
        katasI.sort(key=lambda x: x.player_id.surname)
        katasII = list()
        if not NotKataII:
            katasII = list(Kata.objects.filter(category_id = category))
            for kata in katasII:
                playerT = PlayerTournament.objects.get(player_id = kata.player_id)
                if playerT.acceptedbymanager != True or playerT.acceptedbycoach != True:
                    katasII.remove(kata)
                else:
                    points = list()
                    if kata.point1II != None:
                        points.append(int(kata.point1II))
                    if kata.point2II != None:
                        points.append(int(kata.point2II))
                    if kata.point3II != None:
                        points.append(int(kata.point3II))
                    if kata.point4II != None:
                        points.append(int(kata.point4II))
                    if kata.point5II != None:
                        points.append(int(kata.point5II))
                    if kata.point6II != None:
                        points.append(int(kata.point6II))
                    if kata.point7II != None:
                        points.append(int(kata.point7II))
                    points.sort()
                    if len(points)>2:
                        points.remove(points[0])
                        points.pop()
                        result = 0
                        for point in points:
                            result = result + point
                        kata.resultII = result
                        Kata.objects.filter(id = kata.id).update(resultII = result)
                    else:
                        Kata.objects.filter(id = kata.id).update(resultII = None)
            katasII.sort(key=lambda x: x.resultI, reverse=True)
            katasII = katasII[:7] 
        context = RequestContext(request, {'category': category, 'teams': teams, 'players':players, 'manager':manager, 'katasI':katasI, 'katasII':katasII})
    else:
        context = RequestContext(request, {'category': category, 'teams': teams, 'players':players, 'manager':manager})
    return HttpResponse(template.render(context))

def kyoNextrounds(request, category_id, minround):
    minround = int(minround) + 3
    return redirect('kyoCategory', category_id = category_id, minround = minround)

def kyoPrevrounds(request, category_id, minround):
    if int(minround) != 0:
        minround = int(minround) - 3
    return redirect('kyoCategory', category_id = category_id, minround = minround)

def kyoWinnerFightKM(request, fight_id, whose, minround):
    fight = Fight.objects.get(id= fight_id)
    fights = list(Fight.objects.filter(category_id = fight.category_id, round = fight.round))
    fights.reverse()
    if int(whose) == 0:
        winner = fight.firstplayer.player
    else:
        winner = fight.secondplayer.player 
    if (len(fights)>1 and fight.round!=0) or (len(fights)>0 and fight.round==0) :
        fightsNext = list(Fight.objects.filter(category_id = fight.category_id, round = (fight.round+1)))
        fightsNext.reverse()
        whichIs = fights.index(fight)
        k=2
        playersT = list(fight.category_id.playerT_id.all())
        while k<=len(playersT):
            k=k*2
        i=0
        k=k/2
        while i< fight.round + 1:
            k=k/2
            i = i + 1
        whichWill = int(whichIs/2) - int(k) + int(len(fightsNext))
        print whichWill
        alreadyInNextRound = False
        for fightR in fightsNext:
            if fightR.firstplayer.player.id == fight.firstplayer.player.id or fightR.firstplayer.player.id == fight.secondplayer.player.id:
                alreadyInNextRound = True
                
        print whichWill
        if whichWill >= 0 and alreadyInNextRound == False :
            second = SecondPlayer.objects.create(player = winner)
            Fight.objects.filter(id = fightsNext[whichWill].id).update(secondplayer = second)
        elif whichWill < 0 and alreadyInNextRound == False  :
            first = FirstPlayer.objects.create(player = winner)
            Fight.objects.create(category_id = fight.category_id, firstplayer = first, secondplayer = None, round = (fight.round + 1))
        elif alreadyInNextRound:
            first = FirstPlayer.objects.create(player = winner)
            Fight.objects.filter(id = fightsNext[whichWill].id).update(firstplayer = first)
            
        if (fight.round + 1)%3 == 0:
            minround = int(minround) + 3
        fight.winner = int(whose)
    return redirect('kyoCategory', category_id = fight.category_id.id, minround = minround)

def kyoEditResultsI(request, category_id):
    if 'user' in request.session:
        template = loader.get_template('kyoEditResultsI.html')
        category = Category.objects.get(id = category_id) 
        forms = list()
        katasI = list(Kata.objects.filter(category_id = category))
        for kata in katasI:
            playerT = PlayerTournament.objects.get(player_id = kata.player_id)
            if playerT.acceptedbymanager != True or playerT.acceptedbycoach != True:
                katasI.remove(kata)
               
        katasI.sort(key=lambda x: x.player_id.surname)
        if request.POST:
            form = KyoEditResultsI(request.POST)
            if form.is_valid():
                player = form.cleaned_data['player_id']
                kata = Kata.objects.get(player_id = player)
                form = KyoEditResultsI(request.POST, instance=kata)
                form.save()
                points = list()
                if form.cleaned_data['point1I'] != None:
                    points.append(int(form.cleaned_data['point1I']))
                if form.cleaned_data['point2I'] != None:
                    points.append(int(form.cleaned_data['point2I']))
                if form.cleaned_data['point3I'] != None:
                    points.append(int(form.cleaned_data['point3I']))
                if form.cleaned_data['point4I'] != None:
                    points.append(int(form.cleaned_data['point4I']))
                if form.cleaned_data['point5I'] != None:
                    points.append(int(form.cleaned_data['point5I']))
                if form.cleaned_data['point6I'] != None:
                    points.append(int(form.cleaned_data['point6I']))
                if form.cleaned_data['point7I'] != None:
                    points.append(int(form.cleaned_data['point7I']))
                points.sort()
                if len(points)>2:
                    points.remove(points[0])
                    points.pop()
                    result = 0
                    for point in points:
                        result = result + point
                    Kata.objects.filter(id = kata.id).update(resultI = result)
                else:
                    Kata.objects.filter(id = kata.id).update(resultI = None)
            return redirect('kyoEditResultsI', category_id = category.id)
        else:
            for kata in katasI:
                form = KyoEditResultsI(None, instance=kata)
                form.fields['player_id'].widget.attrs['readonly'] = True
                forms.append(form)
        context = RequestContext(request, {                     
                'forms': forms, 'category': category                                   
            })                                                  
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def kyoEditResultsII(request, category_id):
    if 'user' in request.session:
        template = loader.get_template('kyoEditResultsII.html')
        category = Category.objects.get(id = category_id) 
        forms = list()
        katasI = list(Kata.objects.filter(category_id = category))
        NotKataII = False
        for kata in katasI:
            if kata.resultI == None:
                NotKataII = True
               
        katasI.sort(key=lambda x: x.player_id.surname)
        katasII = list()
        
        if not NotKataII:
            katasII = list(Kata.objects.filter(category_id = category))
            for kata in katasII:
                playerT = PlayerTournament.objects.get(player_id = kata.player_id)
                if playerT.acceptedbymanager != True or playerT.acceptedbycoach != True:
                    katasII.remove(kata)
            katasII.sort(key=lambda x: x.resultI, reverse=True)
            katasII = katasII[:7]
        if request.POST:
            form = KyoEditResultsII(request.POST)
            if form.is_valid():
                player = form.cleaned_data['player_id']
                kata = Kata.objects.get(player_id = player)
                form = KyoEditResultsII(request.POST, instance=kata)
                form.save()
                points = list()
                if form.cleaned_data['point1II'] != None:
                    points.append(int(form.cleaned_data['point1II']))
                if form.cleaned_data['point2II'] != None:
                    points.append(int(form.cleaned_data['point2II']))
                if form.cleaned_data['point3II'] != None:
                    points.append(int(form.cleaned_data['point3II']))
                if form.cleaned_data['point4II'] != None:
                    points.append(int(form.cleaned_data['point4II']))
                if form.cleaned_data['point5II'] != None:
                    points.append(int(form.cleaned_data['point5II']))
                if form.cleaned_data['point6II'] != None:
                    points.append(int(form.cleaned_data['point6II']))
                if form.cleaned_data['point7II'] != None:
                    points.append(int(form.cleaned_data['point7II']))
                points.sort()
                if len(points)>2:
                    points.remove(points[0])
                    points.pop()
                    result = 0
                    for point in points:
                        result = result + point
                    Kata.objects.filter(id = kata.id).update(resultII = result)
                else:
                    Kata.objects.filter(id = kata.id).update(resultII = None)
            return redirect('kyoEditResultsII', category_id = category.id)
        else:
            for kata in katasII:
                form = KyoEditResultsII(None, instance=kata)
                form.fields['player_id'].widget.attrs['readonly'] = True
                forms.append(form)
        context = RequestContext(request, {                     
                'forms': forms, 'category': category                                   
            })                                                  
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
#def kyoAddPlayersToCategory(request, category_id):
#    if 'user' in request.session:
#       template = loader.get_template('kyoAddPlayerToCategory.html')
#        category = Category.objects.get(id=category_id)

def kyoUpdateCategory(request, category_id):
    if 'user' in request.session:
        template = loader.get_template('kyoUpdateCategory.html')
        category = Category.objects.get(id = category_id)
        if request.method == 'POST':
            form = KyoCreateCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()#instance zawiera zapisany obiekt, takze z jego id
                return redirect('kyoCategory', category_id = category.id, minround = 0)
        else:
           form = KyoCreateCategoryForm(None, instance = category)

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
        if category.type=="KM" and category.playerT_id.all().count()>1:
            for fight in Fight.objects.filter(category_id=category):
                firstPlayer = fight.firstplayer
                secondPlayer = fight.secondplayer
                Fight.objects.get(id=fight.id).delete()
                FirstPlayer.objects.get(id = firstPlayer.id).delete()
                if secondPlayer!=None:
                    SecondPlayer.objects.get(id = secondPlayer.id).delete()
            playersT = list(category.playerT_id.all())
            random.shuffle(playersT)
            i = 0
            k=2
            while k<=len(playersT):
                k=k*2
            k=k/2
            if k<len(playersT):
                while i<(len(playersT)-k)*2:
                    first = FirstPlayer.objects.create(player = playersT[i].player_id)
                    i=i+1
                    if i<len(playersT):
                        second = SecondPlayer.objects.create(player = playersT[i].player_id)
                    else: 
                        second = None
                    Fight.objects.create(category_id = category, firstplayer = first, secondplayer = second, round = 0)
                    i=i+1
                while i<len(playersT):
                    first = FirstPlayer.objects.create(player = playersT[i].player_id)
                    i=i+1
                    if i<len(playersT):
                        second = SecondPlayer.objects.create(player = playersT[i].player_id)
                    else: 
                        second = None
                    Fight.objects.create(category_id = category, firstplayer = first, secondplayer = second, round = 1)
                    i=i+1
            else:
                while i<len(playersT):
                    first = FirstPlayer.objects.create(player = playersT[i].player_id)
                    i=i+1
                    if i<len(playersT):
                        second = SecondPlayer.objects.create(player = playersT[i].player_id)
                    else: 
                        second = None
                    Fight.objects.create(category_id = category, firstplayer = first, secondplayer = second, round = 0)
                    i=i+1
    return redirect('kyoTournamentOrganization', tournament_id = tournament.id)

def kyoAddPlayersToCategory(request, category_id):
    if 'user' in request.session:
        template = loader.get_template('kyoAddPlayerToCategory.html')
        category = Category.objects.get(id=category_id)
        players = Player.objects.filter(acceptedbycoachteam=True, acceptedbyplayer=True)
        for categoryT in Category.objects.filter(tournament_id=category.tournament_id):
            if categoryT.type == category.type:
                if categoryT.id == category.id:
                    for playerCat in categoryT.playerT_id.all():
                        players = players.exclude(id=playerCat.player_id.id)
                else:
                    for playerCat in categoryT.playerT_id.filter(acceptedbymanager=True, acceptedbycoach = True):
                        players = players.exclude(id=playerCat.player_id.id)
                        
        context = RequestContext(request, {'category': category, 'players':players })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')

def kyoPlayerToAdd(request, player_id, category_id):
    player = Player.objects.get(id=player_id)
    category = Category.objects.get(id=category_id)
    if PlayerTournament.objects.filter(player_id = player, tournament_id = category.tournament_id):
        playerT = PlayerTournament.objects.get(player_id = player, tournament_id = category.tournament_id)
    else:
        playerT = PlayerTournament.objects.create(player_id=player, tournament_id=category.tournament_id, acceptedbymanager=True, acceptedbycoach=False)
    category.playerT_id.add(playerT)
    if category.type=="KT":
        Kata.objects.create(category_id = category, player_id = player)
    return redirect('kyoAddPlayersToCategory', category_id = category.id)

def kyoPlayerToEnter(request, player_id, category_id):
    player = Player.objects.get(id=player_id)
    category = Category.objects.get(id=category_id)
    if PlayerTournament.objects.filter(player_id = player, tournament_id = category.tournament_id):
        playerT = PlayerTournament.objects.get(player_id = player, tournament_id = category.tournament_id)
    else:
        playerT = PlayerTournament.objects.create(player_id=player, tournament_id=category.tournament_id, acceptedbymanager=False, acceptedbycoach=True)
    category.playerT_id.add(playerT)
    if category.type=="KT":
        Kata.objects.create(category_id = category, player_id = player)
    return redirect('kyoEnterPlayerForCategory', category_id = category.id, user_id = player.team_id.coach.user_id.id)

def kyoDeletePlayerFromCategory(request, player_id, category_id):
    player = Player.objects.get(id = player_id)
    category = Category.objects.get(id = category_id)
    playerT = PlayerTournament.objects.get(player_id=player, tournament_id=category.tournament_id)
    category.playerT_id.remove(playerT)
    if category.type=="KT":
        Kata.objects.filter(category_id = category, player_id = player).delete()
    categories = Category.objects.filter(tournament_id=category.tournament_id)
    contain = False
    for categoryT in categories:
        if playerT in categoryT.playerT_id.all():
            contain = True
    if contain == False:
        tournament = Tournament.objects.get(id = category.tournament_id.id)
        coach = Coach.objects.get(id = Team.objects.get(id = player.team_id.id).coach.id)
        tournament.coaches.remove(coach)
        playerT = PlayerTournament.objects.get(player_id = player, tournament_id=tournament).delete()
    return redirect('kyoCategory', category_id = category.id)

def kyoEnterPlayerForCategory(request, category_id, user_id):
    if 'user' in request.session:
        template = loader.get_template('kyoEnterForCategory.html')
        category = Category.objects.get(id=category_id)
        user = User.objects.get(id=user_id)
        if Coach.objects.filter(user_id=user):
            coach = Coach.objects.get(user_id=user)
            teams = list()
            players = list()
            for team in Team.objects.filter(coach = coach):
                teamTrue = False
                playersC = Player.objects.filter(team_id = team, acceptedbycoachteam=True, acceptedbyplayer=True)
                players2=list()
                for playerC in playersC:
                    players2.append(playerC)
                for categoryT in Category.objects.filter(tournament_id=category.tournament_id):
                    if categoryT.type == category.type:
                        if categoryT.id == category.id:
                            for playerCat in categoryT.playerT_id.all():
                                if playerCat.player_id.team_id == team:
                                    players2.remove(playerCat.player_id)
                        else:
                            for playerCat in categoryT.playerT_id.filter(acceptedbymanager=True, acceptedbycoach = True):
                                if playerCat.player_id.team_id == team:
                                    players2.remove(playerCat.player_id)
                for playerC in players2:
                    teamTrue = True
                if teamTrue:
                    teams.append(team)
                players=players+players2
        context = RequestContext(request, {'category': category, 'players':players, 'teams':teams })
        return HttpResponse(template.render(context))
    else: 
        return redirect('/signIn/')
    
def kyoEnterAllPlayersToCategory(request, category_id, user_id):
    category = Category.objects.get(id=category_id)
    user = User.objects.get(id=user_id)
    if Coach.objects.filter(user_id=user):
            coach = Coach.objects.get(user_id=user)
            players = list()
            for team in Team.objects.filter(coach = coach):
                playersC = Player.objects.filter(team_id = team, acceptedbycoachteam=True, acceptedbyplayer=True)
                for playerC in playersC:
                    players.append(playerC)
                for categoryT in Category.objects.filter(tournament_id=category.tournament_id):
                    if categoryT.type == category.type:
                        if categoryT.id == category.id:
                            for playerCat in categoryT.playerT_id.all():
                                if playerCat.player_id.team_id == team:
                                    players.remove(playerCat.player_id)
                        else:
                            for playerCat in categoryT.playerT_id.filter(acceptedbymanager=True, acceptedbycoach = True):
                                if playerCat.player_id.team_id == team:
                                    players.remove(playerCat.player_id)
            for player in players:
                if PlayerTournament.objects.filter(player_id = player, tournament_id = category.tournament_id):
                    playerT = PlayerTournament.objects.get(player_id = player, tournament_id = category.tournament_id)
                else:
                    playerT = PlayerTournament.objects.create(player_id=player, tournament_id=category.tournament_id, acceptedbymanager=False, acceptedbycoach=True)
                category.playerT_id.add(playerT)
                if category.type=="KT":
                    Kata.objects.create(category_id = category, player_id = player)
    return redirect('/user/')

def kyoEnterPlayersTeamCate(request, team_id, category_id):
    category = Category.objects.get(id=category_id)
    team = Team.objects.get(id=team_id)
    playersC = Player.objects.filter(team_id = team, acceptedbycoachteam=True, acceptedbyplayer=True)
    for categoryT in Category.objects.filter(tournament_id=category.tournament_id):
        if categoryT.type == category.type:
            if categoryT.id == category.id:
                for playerCat in categoryT.playerT_id.all():
                    if playerCat.player_id.team_id == team:
                        playersC = playersC.exclude(id=playerCat.player_id.id)
            else:
                for playerCat in categoryT.playerT_id.filter(acceptedbymanager=True, acceptedbycoach = True):
                    if playerCat.player_id.team_id == team:
                        playersC = playersC.exclude(id=playerCat.player_id.id)
    for player in playersC:
        if PlayerTournament.objects.filter(player_id = player, tournament_id = category.tournament_id):
            playerT = PlayerTournament.objects.get(player_id = player, tournament_id = category.tournament_id)
        else:
            playerT = PlayerTournament.objects.create(player_id=player, tournament_id=category.tournament_id, acceptedbymanager=False, acceptedbycoach=True)
        category.playerT_id.add(playerT)
        if category.type=="KT":
            Kata.objects.create(category_id = category, player_id = player)
    return redirect('kyoEnterPlayerForCategory', category_id = category.id, user_id = team.coach.user_id.id)
