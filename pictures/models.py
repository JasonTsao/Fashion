from django.db import models
from accounts.models import Account


# Create your models here.
class Picture(models.Model):
	owner = models.ForeignKey(Account)
	picture_id = models.CharField(max_length=255, blank=True)
	thumbnail_url = models.CharField(max_length=255, blank=True)
	standard_resolution_url = models.CharField(max_length=255, blank=True)
	low_resolution_url = models.CharField(max_length=255, blank=True)
	ig_link = models.CharField(max_length=255, blank=True)
	picture_file = models.ImageField(upload_to="models/img", null=True)
	rank = models.IntegerField(unique=True, null=True, blank=True)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	location_id = models.CharField(max_length=255, blank=True)
	location_name = models.CharField(max_length=255, blank=True)
	region = models.CharField(max_length=255, blank=True)
	upload_date = models.DateTimeField(null=True,blank=True)
	exists = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		try:
			return str('{0}: {1}'.format(self.owner.username,self.standard_resolution_url)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"


class BrandCategory(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __unicode__(self):
		try:
			return str('{0}'.format(self.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"


class Brand(models.Model):
	category = models.ForeignKey(BrandCategory, null=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	url = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		try:
			return str('{0}: {1}'.format(self.name,self.category.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"


class ArticleCategory(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __unicode__(self):
		try:
			return str('{0}'.format(self.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"


class Article(models.Model):
	category = models.ForeignKey(ArticleCategory, null=True, blank=True)
	brand = models.ForeignKey(Brand, null=True, blank=True)
	name = models.CharField(max_length=255, unique=True)
	url = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		try:
			return str('{0}: {1}: {2}'.format(self.brand.name, self.name,self.category.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"



class Store(models.Model):
	name = models.CharField(max_length=255, unique=True)
	url = models.CharField(max_length=255, blank=True)
	def __unicode__(self):
		try:
			return str('{0}'.format(self.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"


class ArticlePrice(models.Model):
	article = models.ForeignKey(Article)
	price = models.FloatField()
	store = models.ForeignKey(Store, null=True, blank=True)
	def __unicode__(self):
		try:
			return str('{0}: {1}: {2}'.format(self.article.name, self.price,self.store.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"


class PictureArticleTag(models.Model):
	picture = models.ForeignKey(Picture)
	article = models.ForeignKey(Article, null=True, blank=True)
	x_coordinate = models.IntegerField(unique=True, null=True, blank=True)
	y_coordinate = models.IntegerField(unique=True, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		try:
			return str('{0}: {1}: {2}'.format(self.picture.owner.username, self.picture.picture_id, self.article.name)).decode().encode('utf-8')
		except Exception as e:
			print "Can't be displayed"