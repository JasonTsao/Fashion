import json
import logging
import ast
import re
import datetime

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.forms.models import model_to_dict

# Create your views here.
from instagram.utils import getAllFollowing, searchUsersByName
from instagram.api import getProfilePicture
from accounts.models import Account


def submitProfile(request):
	return render_to_response("admin/user_submission/user_submission.html", {}, context_instance=RequestContext(request))
