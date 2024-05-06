from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import secrets




from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
import secrets
import datetime
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.email} -{self.gender} -{self.age}"

class OtpToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp_token")
    otp_code = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField()

    def __str__(self):
        return self.user.username
    

from django.db import models
from django.contrib.auth.models import User

class Predictions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # If you want to associate predictions with users
    image = models.ImageField(upload_to='predictions')
    prediction = models.CharField(max_length=100)  # Adjust the max_length based on the length of your predictions

    def _str_(self):
        return f"Prediction for {self.image.name} by {self.user.username}"  # Customize the string representation as needed
