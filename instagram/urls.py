from django.conf.urls import url, patterns

urlpatterns = patterns("instagram.api",
                        url(r"^oauth$", "OAuth"),
                        url(r"^connect$", "connectInstagram"),
)
