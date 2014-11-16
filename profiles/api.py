import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.forms.models import model_to_dict

from accounts.models import Account
from pictures.models import *


def checkIfUserInDatabase(request):
	rtn_dict = {"success": False, "msg": "", 'ig_id':None, 'exists':None}

	ig_id = request.GET.get('ig_id', False)

	if ig_id:
		rtn_dict['ig_id'] = ig_id
		try:
			ig_model = Account.objects.get(ig_id=ig_id)
			rtn_dict['exists'] = True
		except:
			rtn_dict['exists'] = False
	else:
		rtn_dict['msg'] = 'No ig id provided in GET request'

	return HttpResponse(json.dumps(rtn_dict), "application/json")


def modelProfileDictionary(account):
	try:
		#ig_model = IGModel.objects.get(pk=model_id)
		pictures = Picture.objects.filter(owner=account)
		model_profile = {
			"id": account.id,
			"ig_id": account.ig_id,
			"description": account.description,
			"name": account.username,
			"profile_picture": account.profile_picture,
			"posts": account.posts,
			"followers": account.followers,
			"follows": account.follows,
			"images": []
		}
		for picture in pictures:
			model_profile["images"].append(picture.url)
		return model_profile
	except Exception, e:
		print e
	return False
