import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('auth.urls')),
    url(r'^instagram_api/', include('instagram.urls')),
    # url(r'^$', 'Fashion.views.home', name='home'),
    # url(r'^Fashion/', include('Fashion.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    #IMPORTANT FOR SERVING FILES ON NGINX ON LIVE DEPLOY
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
    {'document_root': settings.STATIC_ROOT, 'show_indexes':True}), 
)
