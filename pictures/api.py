from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.forms.models import model_to_dict

from models import Article, PictureArticleTag, Picture
from accounts.models import Account

import json

PICTURES_PER_PAGE = 20

def paginatedGlobalImages(request):
	rtn_dict = {"success": False}
	try:
		last_id = request.POST.get("lastId", False)
		max_id = 0
		if last_id:
			max_id = int(last_id)
		pictures = Picture.objects.all().order_by('-id')[0:PICTURES_PER_PAGE]
		pic_dict = []
		for picture in pictures:
			pic_dict.append(model_to_dict(picture))
		rtn_dict["response"] = {}
		rtn_dict["response"]["pictures"] = pic_dict
		rtn_dict["response"]["lastId"] = pictures[PICTURES_PER_PAGE - 1].id
		rtn_dict["success"] = True
	except Exception, e:
		rtn_dict["error"] = "{}".format(e)
	return HttpResponse(json.dumps(rtn_dict), "application/json")


def paginatedRegionalImages(request):
	rtn_dict = {"success": False}
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


def modelProfileDictionarySingleImage(account_id):

	try:
		account = Account.objects.get(pk=account_id)
		pictures = Picture.objects.filter(owner=account)
		model_profile = {
			"id": account.id,
			"ig_id": account.ig_id,
			"description": account.description,
			"profile_picture": account.profile_picture,
			"posts": account.posts,
			"followers": account.followers,
			"follows": account.follows,
			"name": account.name,
			"images": pictures[0].standard_resolution_url,
		}
		return model_profile
	except Exception, e:
		print e
	return False


def getUserPictures(request):
	rtn_dict = {"success": False, "msg": "", "user_profile": {}}

	ig_id = request.GET.get('ig_id', False)

	if ig_id:
		try:
			account = Account.objects.get(ig_id=ig_id)
			#initiate profile dictionary and associated dicts
			account_dict = {}
			account_dict['profile'] = model_to_dict(account)
			user_categories_dict = {}
			user_pictures_dict = {}

			try:
				user_pics = Picture.objects.filter(owner=account)
				# assemble counts of user submitted pictures
				for user_pic in user_pics:
					user_pictures_dict[user_pic.picture_id] = {}
					user_pictures_location = {
						'location_id': user_pic.location_id,
						'location_name': user_pic.location_name,
						'latitude': user_pic.latitude,
						'longitude': user_pic.longitude,
					}

					user_pictures_dict[user_pic.picture_id]['id'] = user_pic.picture_id
					user_pictures_dict[user_pic.picture_id]['src'] = user_pic.thumbnail_url
					user_pictures_dict[user_pic.picture_id]['standard_resolution'] = user_pic.standard_resolution_url
					user_pictures_dict[user_pic.picture_id]['low_resolution'] = user_pic.low_resolution_url
					user_pictures_dict[user_pic.picture_id]['ig_link'] = user_pic.ig_link
					user_pictures_dict[user_pic.picture_id]['location'] = user_pictures_location
			except Exception as e:
				print 'Unable to pull user photos: {0}'.format(e)

			# assemble pictures and categories dicts into ig profile dict
			account_dict['pictures'] = user_pictures_dict
			#account_dict['categories'] = user_categories_dict

			try:
				user_pics_array = []
				for k,v in account_dict['pictures'].items():
					user_pics_array.append(v)

				account_dict['pictures'] = user_pics_array
				#account_dict['pictures'] = sorted(user_pics_array, key=lambda x: x["count"], reverse=True)
			except Exception as e:
				print 'Unable to sort pictures: {0}'.format(e)
			
			rtn_dict['user_profile'] = account_dict
		except Exception as e:
			print 'Unable to get IG User submitted profile: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict), "application/json")
