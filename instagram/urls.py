from django.conf.urls import url, patterns

urlpatterns = patterns("instagram.api",
                        url(r"^oauth$", "OAuth"),
                        url(r"^connect$", "connectInstagram"),
                        url(r"^user/follows$", "getIGUserFollowing"),
                        url(r"^user/follow$", "followIGUser"),
                        url(r"^user/relationship$", "checkIGUserRelationship"),
                        url(r"^user/info$", "getIGUserInfo"),
                        url(r"^follows$", "getUserFollowing"),
                        url(r"^search_users$", "searchIGUsersByName"),
                        url(r"^posts$", "getUserPosts"),
                        url(r"^profile/submit$", "submitUserProfile"),
)
