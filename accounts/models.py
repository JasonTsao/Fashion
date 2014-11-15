from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (('female', 'Female'), 
				  ('male', 'Male'),
				  ('both', 'Both'))

# Create your models here.
class Account(models.Model):
	user = models.ForeignKey(User)
	ig_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
	oauth_token = models.CharField(max_length=255, blank=True)
	profile_picture = models.CharField(max_length=255, blank=True)
	access_token = models.CharField(max_length=255, blank=True)
	username = models.CharField(max_length=255, blank=True)
	fullname = models.CharField(max_length=255, blank=True)
	email = models.CharField(max_length=255, blank=True)
	gender = models.CharField(max_length=255, default='female', choices=GENDER_CHOICES)
	web_page = models.CharField(max_length=255, blank=True) 

	#fields that are pulled from instagram directly
	description = models.TextField()
	posts = models.IntegerField(null=True, blank=True)
	followers = models.IntegerField(null=True, blank=True)
	follows = models.IntegerField(null=True, blank=True)

	searchable = models.BooleanField(default=True)
	active = models.BooleanField(default=True)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.user.username