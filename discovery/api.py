from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from models import Article, PictureArticleTag, Picture

import json

PICTURES_PER_PAGE = 20

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
				if last_id:
					article_tags.extends(PictureArticleTag.objects.filter((Q(article=queried_tag)&Q(id__gt=last_id))))
				else:
					article_tags.extends(PictureArticleTag.objects.filter(article=queried_tag))
			article_tags.sort(key=lambda x: x.id, reverse=True)
			rtn_dict["response"] = {"pictures": []}
			picture_ids = []
			count = 0
			for article_tag in article_tag:
				picture = article_tag.picture
				if not article_tag.picture.id in picture_ids:
					picture_ids.append(picture.id)
					rtn_dict["response"]["pictures"].append(model_to_dict(picture))
					count = count + 1
					if count >= PICTURES_PER_PAGE:
						rtn_dict["response"]["lastId"] = picture.id
			rtn_dict["success"] = True
		else:
			rtn_dict["error"] = "No valid query parameters provided in POST data"
	except Exception, e:
		rtn_dict["error"] = "{}".format(e)
	return HttpResponse(json.dumps(rtn_dict), "application/json")
