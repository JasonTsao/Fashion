from django.conf.urls import *
from django.contrib.auth.views import logout
from views import *

urlpatterns += patterns('discovery.api',
	url(r'^api/list$', 'paginatedQueryList'),
)

urlpatterns = patterns('discovery.views',
	url(r'^$', 'discoveryPage'),
)