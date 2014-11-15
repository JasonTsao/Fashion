import oauth2 as oauth
import httplib2
import urllib
import urllib2

import json
import ast
import logging
import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from django.http import HttpResponse, HttpResponseRedirect

from accounts.models import Account

MAX_POST_RETURN = 100
MAX_USER_POST_RETURN = 20

NUM_SEARCH_RESULTS_X_20 = 50

REQUEST_TOKEN_URL = "https://api.instagram.com/oauth/authorize/"
REQUEST_ACCESS_TOKEN = "https://api.instagram.com/oauth/access_token"

CLIENT_ID = '6d7322fc939a4d348dc0cdb1b1b122a8'
CLIENT_SECRET = '48dcf0fcb59f44cabb2a868b647966e8'


@csrf_exempt
def OAuth(request):
	'''
		GET parameters:
			code

		You are redirected here after allowing this app to have api access to your instagram account

		Request access token from instagram
		Save this credentials for user into DB for user

	'''
	rtn_dict = {"success": False, "msg": ""}
	code = request.GET.get('code')
	next = request.GET.get('next', False)

	redirect_uri = 'http://' + request.META['HTTP_HOST'] + '/instagram_api/oauth'

	if next:
		redirect_uri += '?next=' + next

	data = {
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"grant_type": "authorization_code",
		"redirect_uri":redirect_uri,
		"code": code,
	}

	data = urllib.urlencode(data)

	try:
		conn = urllib2.urlopen(REQUEST_ACCESS_TOKEN, data=data)
		try:
			response = json.loads(conn.read())
			print response
			try:
				user = None
				if len(Account.objects.filter(ig_id=response["user"]["id"])) < 1:
					user = User.objects.create_user(username=response["user"]["username"],
													password=response["user"]["id"])
				else:
					account = Account.objects.get(ig_id=response["user"]["id"])
					user = account.user
				account, created = Account.objects.get_or_create(user=user, ig_id=response["user"]["id"])
				#if created:
				account.username = response['user']['username']
				account.profile_picture = response['user']['profile_picture']
				account.access_token = response["access_token"]
				account.fullname = response['user']['full_name']
				account.description = response['user']['bio']
				account.web_page = response['user']['website']
				account.save()
				user = authenticate(username=account.username, password=account.ig_id)
				if user is not None:
					user.backend = 'django.contrib.auth.backends.ModelBackend'
					user.save()
					login(request, user)

					if next:
						return redirect(next)
					else:
						pass
						#return redirect("dashboard.views.dashboard")
					rtn_dict['msg'] = 'Successfully got instagram acess_token'
					rtn_dict['success'] = True
			except Exception as e:
				rtn_dict['error'] = 'Unable to get Instagram access token: {0}'.format(e)
		finally:
			conn.close()
	except urllib2.HTTPError as error:
		print 'Error getting instagram access_token: {0}'.format(error)
		rtn_dict['msg'] = 'Error getting instagram access_token: {0}'.format(error)

	rtn_dict['code'] = code
	
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


@csrf_exempt
def connectInstagram(request):
	'''
		Connect to instagram to start process of getting access token
	'''
	callback_url = 'http://{0}/instagram_api/oauth'.format(request.META["HTTP_HOST"])
	next = request.GET.get('next', False)

	if next:
		callback_url += '?next=' + next

	redirect_url = REQUEST_TOKEN_URL + '?client_id=%s&redirect_uri=%s&response_type=code&scope=likes+comments+relationships' % (CLIENT_ID, urllib.quote_plus(callback_url))

	return HttpResponseRedirect(redirect_url)