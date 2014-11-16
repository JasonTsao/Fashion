import oauth2 as oauth
import urllib
import ast
import json
import urllib2
import urlparse
import requests

from django.http import HttpResponseRedirect, HttpResponse
from random import randint

from accounts.models import Account

NUM_PAGINATIONS = 2


def getPaginationResults(items, response):
	done_paginating = False
	num_times = 0
	while not done_paginating and num_times < NUM_PAGINATIONS:
	#while not done_paginating:
		if response['pagination']:
			conn_pagination = urllib2.urlopen(response['pagination']['next_url'])
			response = json.loads(conn_pagination.read())
			items += response['data']
		else:
			done_paginating = True
		num_times += 1
	return items


def getMasterIGAccount():
    master_account = None
    try:
    	pass
        #master_account = InstagramAccount.objects.filter(master_account=True)[0]
    except Exception as e:
        print 'Unable to get master ig account'

    return master_account

def likePost(post, access_token):
    '''
        Input: 
            post: dictionary of post to be liked
            access_token: access token of user to like with 

        Like the given post with the user authorized by access token
    '''
    like_post_url = 'https://api.instagram.com/v1/media/{0}/likes'.format(post['id'])
    response = False
    data = {
        "access_token": access_token,
    }
    data = urllib.urlencode(data)
    try:
        conn = urllib2.urlopen(like_post_url, data=data)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
        return response
    except urllib2.HTTPError as error:
        print 'Error liking post: {0}'.format(error)    
        return response
    return response


def followUser(ig_id, access_token, action):
    '''
        Input: 
            ig_id: the id of the ig user to follow or unfollow
            access_token: access token of user to follow with 

        Like the given post with the user authorized by access token
    '''
    follow_poster_url = 'https://api.instagram.com/v1/users/{0}/relationship?access_token={1}'.format(ig_id,access_token)
    response = False
    data = {
        'access_token': access_token,
        'action': action,
    }
    data = urllib.urlencode(data)
    try:
        conn = urllib2.urlopen(follow_poster_url, data=data)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()

        return response
    except urllib2.HTTPError as error:
        print 'Error following user: {0}'.format(error) 
        return response
    return response


def getIGUserRelationship(ig_id, access_token):
	'''
        Input: 
            ig_id: the id of the ig user to get the relationship of
            access_token: access token of user to get relationship with 

		Find the relationship between the user authorized by access token
	'''
	find_relationship_url = 'https://api.instagram.com/v1/users/{0}/relationship?access_token={1}'.format(ig_id,access_token)
	response = False
	try:
		conn = urllib2.urlopen(find_relationship_url)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()

		return response
	except urllib2.HTTPError as error:
		print 'Error following user: {0}'.format(error) 
		return response
	return response



def searchMostRecentHashtags(search_term, access_token):
    '''
        Input: 
            search_term: tag to look for in recent instagram posts
            access_token: instagram access token of user authorized to search for hashtags
        Output:
            posts_containing_tags: list of dictionaries of posts containing search term

        Get 1000 posts containing search term
    '''
    posts_containing_tags = []
    try:
        search_term = search_term.strip()
        search_hashtags_url = 'https://api.instagram.com/v1/tags/{0}/media/recent?access_token={1}'.format(search_term,access_token)
        try:
            #for x in range(0, NUM_SEARCH_RESULTS_X_20)
            for x in range(0,2):
                conn = urllib2.urlopen(search_hashtags_url)
                try:
                    response = json.loads(conn.read())
                    search_hashtags_url = response['pagination']['next_url']
                    posts_containing_tags += response['data']
                finally:
                    conn.close()
        except urllib2.HTTPError as error:
            print 'Error getting instagram access_token: {0}'.format(error)
    except Exception as e:
        print 'Unable to find search results for {0}: {1}'.format(search_term,e)

    return posts_containing_tags


def getIGUserData(user_id, access_token):
	profile = {}
	try:
		ig_user_data_url = 'https://api.instagram.com/v1/users/{0}/?access_token={1}'.format(user_id, access_token)

		try:
			conn = urllib2.urlopen(ig_user_data_url)
			try:
				response = json.loads(conn.read())
				profile = response['data']
			finally:
				conn.close()
		except urllib2.HTTPError as error:
			print 'Error getting users {0} follows: {1}'.format(user_id, error)
	except Exception as e:
		print 'Unable to find users that this user is following: {0}'.format(e)

	return profile


def getAllFollowing(user_id, access_token):
	#follows = []
	response = {}
	try:
		search_follows_url = 'https://api.instagram.com/v1/users/{0}/follows?access_token={1}'.format(user_id, access_token)

		try:
			conn = urllib2.urlopen(search_follows_url)
			try:
				response = json.loads(conn.read())
				#follows = response['data']

				#if response['pagination']:
					#pass
					#follows = getPaginationResults(follows, response)

			finally:
				conn.close()
		except urllib2.HTTPError as error:
			print 'Error getting users {0} follows: {1}'.format(user_id, error)
	except Exception as e:
		print 'Unable to find users that this user is following: {0}'.format(e)

	return response


def getMostFollowedUsers(user_id, num_return, access_token):
	highest_followed = []

	try:
		response = getAllFollowing(user_id, access_token)

		follows = response['data']

		for user in follows:
			user_follows = getAllFollowing(user['id'], access_token)
			num_followers = len(user_follows)

		search_follows_url = 'https://api.instagram.com/v1/users/{0}/follows?access_token={1}'.format(user_id, access_token)

	except Exception as e:
		print 'Unable to find users that this user is following: {0}'.format(e)

	return highest_followed


def searchUsersByName(user_name, access_token):
	'''
		Input:
			user_name: user name to be used as search term
			access_token: token of validated user to perform search

		Output:
			users: an array with users returned by IG when you search using "user_name"

		Search instagram for users using the search term "user_name"
	'''
	user_id = ''
	user_name = user_name.strip()
	users = []
	try:
		search_url = 'https://api.instagram.com/v1/users/search?q={0}&access_token={1}'.format(user_name, access_token)
		try:
			conn = urllib2.urlopen(search_url)
			#getting following users
			try:
				response = json.loads(conn.read())
				users = response['data']
			finally:
				conn.close()
		except urllib2.HTTPError as error:
			print 'Error getting instagram access_token: {0}'.format(error)

	except Exception as e:
		print 'Unable to find search results for {0}: {1}'.format(user_name,e)

	return users


def getIGUserPosts(user_id, access_token, filter_type="all"):
	response = {}
	try:
		search_posts_url = 'https://api.instagram.com/v1/users/{0}/media/recent/?access_token={1}'.format(user_id, access_token)
		try:
			conn = urllib2.urlopen(search_posts_url)
			try:
				response = json.loads(conn.read())
				#posts = response['data']

				'''
				if response['pagination']:
					posts = getPaginationResults(posts, response)
				'''
			finally:
				conn.close()
		except urllib2.HTTPError as error:
			print 'Error getting instagram access_token: {0}'.format(error)
	except Exception as e:
		print 'Unable to search posts for user {0}: {1}'.format(user_id, e)
	return response


def getAuthenticatedUserPosts(user_id, access_token, filter_type="most_recent"):
	''' 
		FOR USE LATER WHEN USERS WANT TO AUTHENTICATE FOR US SO WE CAN SEE PRIVATE PICTURES
	'''

	posts = []
	try:
		search_posts_url = 'https://api.instagram.com/v1/users/self/feed?access_token={0}'.format(access_token)
		try:
			conn = urllib2.urlopen(search_posts_url)
			try:
				response = json.loads(conn.read())
				posts = response['data']

				if response['pagination']:
					posts = getPaginationResults(posts, response)
			finally:
				conn.close()
		except urllib2.HTTPError as error:
			print 'Error getting instagram access_token: {0}'.format(error)
	except Exception as e:
		print 'Unable to search posts for user {0}: {1}'.format(user_id, e)
	return posts