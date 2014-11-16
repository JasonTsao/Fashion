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
from models import Picture


def picturePage(request):
	picture_id = request.GET.get('picture_id', False)
	ig_id = request.GET.get('ig_id', False)
	picture = None
	picture_count = 1
	user_voted = False
	page_name = False

	print 'picture_id : {0}'.format(picture_id)
	print 'ig_id: {0}'.format(ig_id)

	if picture_id and ig_id:
		try:
			ig_model = Account.objects.get(ig_id=ig_id)
			page_name = ig_model.username
			try:
				picture = Picture.objects.get(picture_id=picture_id)
			except Exception as e:
				print 'Unable to get user picture: {0}'.format(e)

		except Exception as e:
			print 'Unable to pull IG user profile: {0}'.format(e)

	print 'picture'
	print picture

	pf_pic = getProfilePicture(request)

	if request.is_mobile:
		return render_to_response("mobile/pictures/picture.html", {"picture": picture, "ig_model": ig_model, "pf_pic": pf_pic, 'page_name':page_name}, context_instance=RequestContext(request))
	else:
		return render_to_response("mobile/pictures/picture.html", {"picture": picture, "ig_model": ig_model, "pf_pic": pf_pic, 'page_name':page_name}, context_instance=RequestContext(request))
