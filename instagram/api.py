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


def getProfilePicture(request):
	pf_pic = False
	try:
		account = Account.objects.get(user=request.user)
		pf_pic = account.profile_picture
	except:
		pass
	return pf_pic


def updateUserSocialData(ig_profile):
	try:
		account = Account.objects.get(ig_id=ig_profile['id'])
		account.profile_picture = ig_profile['profile_picture']
		account.posts = ig_profile['counts']['media']
		account.followers = ig_profile['counts']['followed_by']
		account.follows = ig_profile['counts']['follows']
		account.description = ig_profile['bio']
		account.save()
	except Exception as e:
		print 'Unable to update instagram user profile picture: {0}'.format(e)


@login_required
def checkIGUserRelationship(request):
	rtn_dict = {'success':False, 'msg': ''}
	try:
		ig_id = request.GET.get('ig_id', False)

		if ig_id:
			account = Account.objects.get(user=request.user)
			relationship = getIGUserRelationship(ig_id, account.access_token)
			rtn_dict['success'] = True
			rtn_dict['relationship'] = relationship
			rtn_dict['msg'] = 'Successfully checked relationship with user: {0}'.format(ig_id)
		else:
			rtn_dict['msg'] = 'No ig id in GET request parameters'
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get IG user relationship: {0}'.format(e)
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


@login_required
def followIGUser(request):
	rtn_dict = {'success':False, 'msg': ''}
	try:
		ig_id = request.POST.get('ig_id', False)
		action = request.POST.get('action', False)

		if ig_id and action:
			account = Account.objects.get(user=request.user)
			follows = followUser(ig_id, account.access_token, action)
			rtn_dict['success'] = True
			rtn_dict['msg'] = 'Successfully followed user with id: {0}'.format(ig_id)
		else:
			rtn_dict['msg'] = 'No ig id in GET request parameters'
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get list of users that you follow: {0}'.format(e)
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


@login_required
def getUserFollowing(request):
	rtn_dict = {'success':False, 'msg': ''}
	try:
		account = Account.objects.get(user=request.user)
		response = getAllFollowing(account.ig_id, account.access_token)
		follows = response['data']
		rtn_dict['follows'] = follows
		rtn_dict['pagination'] = response['pagination']
		rtn_dict['follows_count'] = len(follows)
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get list of users that you follow: {0}'.format(e)
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


@login_required
def getIGUserInfo(request):
	rtn_dict = {'success':False, 'msg': ''}
	try:
		ig_id = request.GET.get('ig_id', False)

		if ig_id:
			account = Account.objects.get(user=request.user)
			ig_profile = getIGUserData(ig_id, account.access_token)

			updateUserSocialData(ig_profile)
			rtn_dict['ig_profile'] = ig_profile
			rtn_dict['success'] = True
		else:
			rtn_dict['msg'] = 'No ig id in GET request parameters'
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get list of users that you follow: {0}'.format(e)
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


@login_required
def getIGUserFollowing(request):
	rtn_dict = {'success':False, 'msg': ''}
	try:
		ig_user_id = request.GET.get('ig_id', False)

		if ig_user_id:
			account = Account.objects.get(user=request.user)
			follows = getAllFollowing(ig_user_id, account.access_token)
			rtn_dict['follows'] = follows
			rtn_dict['follows_count'] = len(follows)
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get list of users that you follow: {0}'.format(e)
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


@login_required
def searchIGUsersByName(request):
	rtn_dict = {'success':False, 'msg': ''}

	try:
		search_name = request.POST['search_name']

		account = Account.objects.get(user=request.user)
		ig_users = searchUsersByName(search_name, account.access_token)

		rtn_dict['ig_users'] = ig_users
		rtn_dict['ig_users_count'] = len(ig_users)
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get list of users that you follow: {0}'.format(e)
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


@login_required
def getUserPosts(request):
	rtn_dict = {'success':False, 'msg': ''}
	try:
		user_id = request.POST['user_id']
		post_filter = request.POST['post_filter']
		account = Account.objects.get(user=request.user)
		response = getIGUserPosts(user_id, account.access_token, post_filter)
		posts = response['data']

		rtn_dict['posts'] = posts
		rtn_dict['pagination'] = response['pagination']
		rtn_dict['posts_count'] = len(posts);
		rtn_dict['success'] = True;
	except Exception as e:
		rtn_dict['msg'] = 'Unable to get posts from user {0}: {1}'.format(user_id, e)
	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")