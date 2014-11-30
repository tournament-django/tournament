from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

# Create your views here.

def KarateShotokanMain(request):
    template = loader.get_template('shotokan-main.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))