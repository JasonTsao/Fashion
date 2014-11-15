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
    # url(r'^$', 'Fashion.views.home', name='home'),
    # url(r'^Fashion/', include('Fashion.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    #IMPORTANT FOR SERVING FILES ON NGINX ON LIVE DEPLOY
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
    {'document_root': settings.STATIC_ROOT, 'show_indexes':True}), 
)
