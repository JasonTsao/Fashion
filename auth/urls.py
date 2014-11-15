from django.conf.urls import *
from django.contrib.auth.views import logout
from views import *

urlpatterns = patterns('',
	url(r'register', 'auth.views.register'),
	url(r'login', 'auth.views.login_func'),
    # url(r'account_settings', 'auth.views.account_settings'),
    # url(r'change_password', 'auth.views.change_password'),
    # url(r'change_email', 'auth.views.change_email'),

    #url(r'logout/$', 'django.contrib.auth.views.logout', {"next_page": '/logout'}, name="ighottest.logout"),
    
    # url(r'user/(\d+)', 'auth.views.user_overview'),
)