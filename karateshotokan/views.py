from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from karateshotokan.forms import CreateTournamentFormShotokan, ChooseTournamentFormShotokan, CreateTeamFormShotokan
from karateshotokan.models import Document
from main.forms import User, Manager, Coach, Manager, Team
from main.models import Tournament
# Create your views here.

def KarateShotokanMain(request):
    template = loader.get_template('shotokan-main.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def KarateShotokanCreate(request):
    if 'user' in request.session:
        template = loader.get_template('createTournamentShotokan.html')

        if request.method == 'POST':
            form = CreateTournamentFormShotokan(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.session['user'])
                instance=form.save()#instance zawiera zapisany obiekt, takze z jego id
                Manager.objects.create(user_id=user, tournament = instance)
                return redirect('/user/')
        else:
           form = CreateTournamentFormShotokan()

        context = RequestContext(request, dict(form=form))
        return HttpResponse(template.render(context))
    else:
        return redirect('/signIn/')
    
    
def shoTournamentOrganization(request, tournament_id):
    template = loader.get_template('shoTournamentOrganization.html')
    tournament = Tournament.objects.get(id=tournament_id)
    
    context = RequestContext(request, {'tournament': tournament })
    return HttpResponse(template.render(context))


def KarateShotokanChoose(request):
    if 'user' in request.session:
        template = loader.get_template('chooseTournamentShotokan.html')

        if request.method == 'POST':
            form = ChooseTournamentFormShotokan(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.session['user'])
                instance=form.save()#instance zawiera zapisany obiekt, takze z jego id
                Manager.objects.create(user_id=user, tournament = instance)
                return redirect('/user/')
        else:
           form = ChooseTournamentFormShotokan()

        context = RequestContext(request, dict(form=form))
        return HttpResponse(template.render(context))
    else:
        return redirect('/signIn/')

def KarateShotokanCreateTeam(request):
    if 'user' in request.session:
        template = loader.get_template('createTeamShotokan.html')

        if request.method == 'POST':
            form = CreateTeamFormShotokan(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.session['user'])
                instance=form.save()#instance zawiera zapisany obiekt, takze z jego id
                coachobj, bool= Coach.objects.get_or_create(user_id=user, defaults={'name': user.name, 'surname': user.surname})
                Team.objects.filter(id = instance.id).update(coach = coachobj)
                return redirect('/user/')
        else:
           form = CreateTeamFormShotokan()

        context = RequestContext(request, {
            'form': form,
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('/signIn/')
