from django.urls import path
from .views import (
    SignUpView,
    ActivateView,
    AboutView,
    LoginView,
    SearchUserAPIView,
    SendFriendRequestAPIView,
    RespondFriendRequestAPIView,
    ListFriendsAPIView,
    ListPendingFriendRequestsAPIView,
    CustomObtainAuthToken,
)

urlpatterns = [
    path("token-auth/", CustomObtainAuthToken.as_view(), name="api_token_auth"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("about/", AboutView.as_view(), name="about"),
    path("search/", SearchUserAPIView.as_view(), name="search"),
    path(
        "friend-request/send/<int:user_id>/",
        SendFriendRequestAPIView.as_view(),
        name="send-friend-request",
    ),
    path(
        "friend-request/respond/<int:request_id>/<str:action>/",
        RespondFriendRequestAPIView.as_view(),
        name="respond-friend-request",
    ),
    path("friends/", ListFriendsAPIView.as_view(), name="list-friends"),
    path(
        "friend-requests/pending/",
        ListPendingFriendRequestsAPIView.as_view(),
        name="list-pending-friend-requests",
    ),
]
