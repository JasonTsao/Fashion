from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("profiles.views",
			url(r"^submit$", "submitProfile"),
)

urlpatterns += patterns("profiles.api",
        url(r"^exists$", "checkIfUserInDatabase"),

)

