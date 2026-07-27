from django.db import models


# =========================================================
# USER — a plain model (no passwords/permissions)
# =========================================================
# If you ever need the built-in auth user instead, import it with
#   from django.contrib.auth.models import User
# and set AUTH_USER_MODEL in settings BEFORE the first migrate.
class User(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.phone_number}'
