from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Check if a new user is created

        subject = "Welcome to Our Website"
        message = f"Hi {instance.first_name}, thank you for registering at our site."

        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, email_from, recipient_list)
