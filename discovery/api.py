from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from models import Article, PictureArticleTag

import json


def paginatedQueryList(request):
	rtn_dict = {"success": False}
	try:
		last_id = request.POST.get("lastId", False)
		brand_ids = request.POST.getlist("brandIds[]", False)
		article_ids = request.POST.getlist("articleIds[]", False)
		if brand_ids or article_ids:
			queried_tags = []
			for brand_id in brand_ids:
				queried_tags = Article.objects.filter(brand__id=brand_id)
			for article_id in article_ids:
				queried_tags.extends(Article.objects.filter(category__id=article_id))
			article_tags = []
			for queried_tag in queried_tags:
				article_tags.extends(PictureArticleTag.objects.filter(article=queried_tag))
			rtn_dict["response"] = {"pictures": []}
			for article_tag in article_tag:
				rtn_dict["response"]["pictures"].append(model_to_dict(article_tag.picture))
			rtn_dict["success"] = True
		else:
			rtn_dict["error"] = "No valid query parameters provided in POST data"
	except Exception, e:
		rtn_dict["error"] = "{}".format(e)
	return HttpResponse(json.dumps(rtn_dict), "application/json")
