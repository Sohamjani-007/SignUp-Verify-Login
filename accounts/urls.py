from django.urls import path
from .views import SignUpView, ActivateView, AboutView, LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('about/', AboutView.as_view(), name='about'),
]
