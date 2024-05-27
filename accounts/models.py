from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import FriendRequestStatusChoices

# Create your models here.


class CustomUser(AbstractUser):
    """
    AbstractUser has all the remaining fields (Inherits)
    Adding mobile and email_verification fields here to let store in DB.
    """

    mobile = models.CharField(max_length=15)
    email_verified = models.BooleanField(default=False)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name="sent_requests", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name="received_requests", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=FriendRequestStatusChoices.choices,
        default=FriendRequestStatusChoices.pending,
    )

    class Meta:
        unique_together = ("from_user", "to_user")
