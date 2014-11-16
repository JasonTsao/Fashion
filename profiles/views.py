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
from pictures.models import Picture


def submitProfile(request):
	if request.is_mobile:
		#SHOULD REALLY SEND THEM TO A DEFAULT PAGE
		return render_to_response("mobile/admin/user_submission/user_submission.html", {}, context_instance=RequestContext(request))
	else:
		return render_to_response("desktop/admin/user_submission/user_submission.html", {}, context_instance=RequestContext(request))


def profilePage(request):
	ig_id = request.GET.get('ig_id', False)
	ig_model = None
	tags_dict = {}
	submitted_count = None
	competitions = []
	votes = []
	page_name = False

	if ig_id:
		try:
			account = Account.objects.get(ig_id=ig_id)
			page_name = account.username

			'''
			try:
				competition_objs = Competition.objects.filter(competitor__model=ig_model)

				for competition in competition_objs:
					competition_dict = {
						'id':competition.id,
						'name':competition.name,
						'wins': {},
						'losses': {},
						'total_wins': 0,
						'total_losses': 0,
					}

					competition_votes = CompetitionVote.objects.select_related().filter(Q(competition=competition), Q(winner__model=ig_model)| Q(loser__model=ig_model))
					votes = competition_votes
					for vote in competition_votes:
						if vote.winner.model == ig_model:
							try:
								competition_dict['wins'][vote.loser.model.ig_id]['count'] += 1
								competition_dict['total_wins'] +=1
							except:
								winner_dict = {
									'ig_id': vote.loser.model.ig_id,
									'name': vote.loser.model.name,
									'profile_picture': vote.loser.model.profile_picture,
									'count': 1
								}
								competition_dict['wins'][vote.loser.model.ig_id] = winner_dict
								competition_dict['total_wins'] +=1
						elif vote.loser.model == ig_model:
							try:
								competition_dict['losses'][vote.winner.model.ig_id]['count'] += 1
								competition_dict['total_losses'] +=1
							except:
								loser_dict = {
									'ig_id': vote.winner.model.ig_id,
									'name': vote.winner.model.name,
									'profile_picture': vote.winner.model.profile_picture,
									'count': 1
								}
								competition_dict['losses'][vote.winner.model.ig_id] = loser_dict
								competition_dict['total_losses'] +=1

					#Sort Wins and Losses
					try:
						wins_array = []
						for k,v in competition_dict['wins'].items():
							wins_array.append(v)
						competition_dict['wins'] = sorted(wins_array, key=lambda x: x["count"], reverse=True)
					except Exception as e:
						print 'Unable to sort wins: {0}'.format(e)

					try:
						losses_array = []
						for k,v in competition_dict['losses'].items():
							losses_array.append(v)
						competition_dict['losses'] = sorted(losses_array, key=lambda x: x["count"], reverse=True)
					except Exception as e:
						print 'Unable to sort losses: {0}'.format(e)
					#competition_dict['losses'] = sorted(competition_dict['losses'], key=lambda x: x["count"], reverse=True)
					#competition_dict['wins'] = sorted(competition_dict['wins'], key=lambda x: x["count"], reverse=True)

					competitions.append(competition_dict)
			except Exception as e:
				print 'Unable to get competition data for user: {0}'.format(e)
			'''

		except Exception as e:
			print 'Unable to pull IG user profile: {0}'.format(e)

	pf_pic = getProfilePicture(request)

	if request.is_mobile:
		return render_to_response("mobile/profiles/profile.html", {"ig_model":ig_model, "pf_pic": pf_pic, 'page_name':page_name}, context_instance=RequestContext(request))
	else:
		#switch to point to desktop page when we have one!
		#return render_to_response("desktop/profiles/profile.html", {"ig_model":ig_model, "pf_pic": pf_pic, 'page_name':page_name}, context_instance=RequestContext(request))
		return render_to_response("mobile/profiles/profile.html", {"ig_model":ig_model, "pf_pic": pf_pic, 'page_name':page_name}, context_instance=RequestContext(request))
