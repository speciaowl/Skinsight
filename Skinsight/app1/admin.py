from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry  # Import the LogEntry model
from .models import OtpToken
from .models import UserDetails
from .models import Predictions

# Unregister the LogEntry model from the admin site
# admin.site.unregister(LogEntry)



class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")

admin.site.register(OtpToken, OtpTokenAdmin)

admin.site.register(UserDetails)

admin.site.register(Predictions)