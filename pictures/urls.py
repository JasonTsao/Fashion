from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("pictures.views",
			url(r"^$", "picturePage"),
)

urlpatterns += patterns("pictures.api",
        url(r"^get$", "getUserPictures"),

)

