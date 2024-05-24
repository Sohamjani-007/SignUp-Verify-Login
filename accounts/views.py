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


User = get_user_model()


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            return render(request, 'accounts/signup.html', {'form': form, 'message': 'User registered successfully. Please verify your email.'})
        return render(request, 'accounts/signup.html', {'form': form})


def send_verification_email(request, user):
    """
    Retrieve the current site's domain using get_current_site(request).
    Prepare the email subject and the message body using render_to_string, incorporating user details and verification token.
    Encode the user's ID using urlsafe_base64_encode(force_bytes(user.pk)).
    Generate a verification token for the user with default_token_generator.make_token(user).
    Send the email using send_mail with the prepared subject, message, sender's email, and recipient's email.
    """
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('accounts/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, 'sohamjani007@gmail.com', [user.email])


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
            return redirect(reverse_lazy('login'))  # Redirect to login page
        else:
            return render(request, 'accounts/activation_invalid.html')


class LoginView(View):
    def get(self, request):
        """
        Loading the Preview Login Form using this GET endpoint.
        """
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        """
        Checking the validity of User.
        """
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('about')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, 'accounts/login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AboutView(View):
    def get(self, request):
        return render(request, 'accounts/about.html')
