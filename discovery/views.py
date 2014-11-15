# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

def discoveryPage(request):
	return render_to_response("discovery/main.html", {}, context_instance=RequestContext(request))