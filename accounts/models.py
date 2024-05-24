from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class CustomUser(AbstractUser):
    """
    AbstractUser has all the remaining fields (Inherits)
    Adding mobile and email_verification fields here to let store in DB.
    """
    mobile = models.CharField(max_length=15)
    email_verified = models.BooleanField(default=False)
