# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Picture'
        db.create_table(u'pictures_picture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('picture_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('thumbnail_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('standard_resolution_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('low_resolution_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ig_link', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('picture_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('location_id', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('location_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('exists', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pictures', ['Picture'])

        # Adding model 'BrandCategory'
        db.create_table(u'pictures_brandcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'pictures', ['BrandCategory'])

        # Adding model 'Brand'
        db.create_table(u'pictures_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.BrandCategory'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'pictures', ['Brand'])

        # Adding model 'ArticleCategory'
        db.create_table(u'pictures_articlecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'pictures', ['ArticleCategory'])

        # Adding model 'Article'
        db.create_table(u'pictures_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.ArticleCategory'], null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.Brand'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'pictures', ['Article'])

        # Adding model 'Store'
        db.create_table(u'pictures_store', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'pictures', ['Store'])

        # Adding model 'ArticlePrice'
        db.create_table(u'pictures_articleprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.Article'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.Store'], null=True, blank=True)),
        ))
        db.send_create_signal(u'pictures', ['ArticlePrice'])

        # Adding model 'PictureArticleTag'
        db.create_table(u'pictures_picturearticletag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('picture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.Picture'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pictures.Article'], null=True, blank=True)),
            ('x_coordinate', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('y_coordinate', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pictures', ['PictureArticleTag'])


    def backwards(self, orm):
        # Deleting model 'Picture'
        db.delete_table(u'pictures_picture')

        # Deleting model 'BrandCategory'
        db.delete_table(u'pictures_brandcategory')

        # Deleting model 'Brand'
        db.delete_table(u'pictures_brand')

        # Deleting model 'ArticleCategory'
        db.delete_table(u'pictures_articlecategory')

        # Deleting model 'Article'
        db.delete_table(u'pictures_article')

        # Deleting model 'Store'
        db.delete_table(u'pictures_store')

        # Deleting model 'ArticlePrice'
        db.delete_table(u'pictures_articleprice')

        # Deleting model 'PictureArticleTag'
        db.delete_table(u'pictures_picturearticletag')


    models = {
        u'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'followers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'follows': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'female'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ig_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'posts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'web_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'codename',)", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pictures.article': {
            'Meta': {'object_name': 'Article'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.Brand']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.ArticleCategory']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'pictures.articlecategory': {
            'Meta': {'object_name': 'ArticleCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'pictures.articleprice': {
            'Meta': {'object_name': 'ArticlePrice'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.Article']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.Store']", 'null': 'True', 'blank': 'True'})
        },
        u'pictures.brand': {
            'Meta': {'object_name': 'Brand'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.BrandCategory']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'pictures.brandcategory': {
            'Meta': {'object_name': 'BrandCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'pictures.picture': {
            'Meta': {'object_name': 'Picture'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ig_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'low_resolution_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Account']"}),
            'picture_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'picture_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'standard_resolution_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'thumbnail_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pictures.picturearticletag': {
            'Meta': {'object_name': 'PictureArticleTag'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.Article']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pictures.Picture']"}),
            'x_coordinate': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'y_coordinate': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'pictures.store': {
            'Meta': {'object_name': 'Store'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['pictures']