from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.forms.models import model_to_dict

from models import Article, PictureArticleTag, Picture

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