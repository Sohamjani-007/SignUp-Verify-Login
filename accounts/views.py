from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .choices import FriendRequestStatusChoices


User = get_user_model()


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        user = token.user
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            return render(
                request,
                "accounts/signup.html",
                {
                    "form": form,
                    "message": "User registered successfully. Please verify your email.",
                },
            )
        return render(request, "accounts/signup.html", {"form": form})


def send_verification_email(request, user):
    """
    Retrieve the current site's domain using get_current_site(request).
    Prepare the email subject and the message body using render_to_string, incorporating user details and verification token.
    Encode the user's ID using urlsafe_base64_encode(force_bytes(user.pk)).
    Generate a verification token for the user with default_token_generator.make_token(user).
    Send the email using send_mail with the prepared subject, message, sender's email, and recipient's email.
    """
    current_site = get_current_site(request)
    subject = "Activate Your Account"
    message = render_to_string(
        "accounts/account_activation_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    send_mail(subject, message, "sohamjani007@gmail.com", [user.email])


class ActivateView(View):
    """
    Decodes the user ID from a base64 encoded string.
    Retrieves the corresponding user from the database.
    Checks the validity of the activation token.
    Activates the user account if the token is valid.
    Logs the user in and redirects to the login page if activation is successful.
    Renders an error page if activation fails.
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Strategy object used to generate and check tokens for the password
        # reset mechanism.
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_verified = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy("login"))  # Redirect to login page
        else:
            return render(request, "accounts/activation_invalid.html")


class LoginView(View):
    def get(self, request):
        """
        Loading the Preview Login Form using this GET endpoint.
        """
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        """
        Checking the validity of User.
        """
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("about")
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, "accounts/login.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class AboutView(View):
    def get(self, request):
        return render(request, "accounts/about.html")


class SearchUserPagination(PageNumberPagination):
    """
    This class customizes pagination settings,
    allowing API responses to be paginated in a flexible manner based on client requests.

    # When a client makes a request to this view, they can control pagination using the `page` and `page_size` query parameters.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SearchUserAPIView(generics.ListAPIView):
    """
    # Assuming the API view is hooked to a URL, you can perform a GET request like:
    GET /api/users/search?q=john
    # This will return a list of users whose email, first name, or last name contains 'john' in a case-insensitive manner
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SearchUserPagination

    def get_queryset(self):
        keyword = self.request.query_params.get("q", None)
        if keyword:
            return CustomUser.objects.filter(
                Q(email__iexact=keyword)
                | Q(first_name__icontains=keyword)
                | Q(last_name__icontains=keyword)
            )
        return CustomUser.objects.none()


class SendFriendRequestThrottle(UserRateThrottle):
    """
    The SendFriendRequestThrottle class is a custom throttling class that limits the rate at
    which users can send friend requests to three requests per minute.

    1) Assuming the SendFriendRequestAPIView is set up and running
    2) A user tries to send more than three friend requests in a minute
    3) The fourth request within the same minute will be throttled, and an appropriate response will be returned.
    """

    rate = "3/minute"


class SendFriendRequestAPIView(APIView):
    """
    Assuming the API endpoint is set up at /users/{user_id}/send_friend_request/
    A POST request to this endpoint with a valid authenticated session will attempt to send a friend request to the user specified by `user_id`.
    If successful, it returns HTTP 201 with a message "Friend request sent."
    If a request is already sent or if a user tries to send a request to themselves, it returns HTTP 400 with an appropriate error message.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [SendFriendRequestThrottle]

    def post(self, request, user_id):
        from_user = request.user
        to_user = get_object_or_404(CustomUser, id=user_id)

        if from_user == to_user:
            return Response(
                {"error": "You cannot send a friend request to yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )

        if created:
            return Response(
                {"message": "Friend request sent."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Friend request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RespondFriendRequestAPIView(APIView):
    """
    # Assuming the API endpoint is configured at /api/respond-friend-request/<request_id>/<action>/
    # To accept a friend request with ID 1:
    POST /api/respond-friend-request/1/accept/
    # To reject a friend request with ID 1:
    POST /api/respond-friend-request/1/reject/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, request_id, action):
        friend_request = get_object_or_404(
            FriendRequest, from_user=request_id, to_user=request.user
        )

        if action == "accept":
            friend_request.status = FriendRequestStatusChoices.accepted
            friend_request.save()
            return Response(
                {"message": "Friend request accepted."}, status=status.HTTP_200_OK
            )
        elif action == "reject":
            friend_request.status = FriendRequestStatusChoices.rejected
            friend_request.save()
            return Response(
                {"message": "Friend request rejected."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST
            )


class ListFriendsAPIView(APIView):
    """
    # Assuming the API view is hooked to a URL, a client would make a GET request to this API.
    # The response would contain a list of user objects that represent the friends of the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get all accepted friend requests where the user is either the sender or the receiver
        accepted_requests = FriendRequest.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status=FriendRequestStatusChoices.accepted,
        )

        friends = []
        # lets loop the all found objects i.e friends
        for request in accepted_requests:
            if request.from_user == user:
                friends.append(request.to_user)
            else:
                friends.append(request.from_user)

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListPendingFriendRequestsAPIView(generics.ListAPIView):
    """
    # Assuming the API view is hooked to a URLconf at '/api/friend-requests/pending/'
    # A GET request to this endpoint would return a JSON list of pending friend requests for the authenticated user.
    """

    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            to_user=self.request.user, status=FriendRequestStatusChoices.pending
        )
