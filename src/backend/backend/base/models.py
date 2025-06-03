from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.postgres.fields import JSONField

class User(AbstractUser):
    USERNAME_FIELD = "username"

    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class PosTerminal(User):
    # AUTH_BACKENDS = "backend.auth.TerminalAuthBackend"

    phone = models.CharField(max_length=20, blank=True, null=True)
    pin = models.CharField("Terminal PIN", max_length=10, null=True, blank=True)

    def __str__(self):
        return self.username

class GuurUser(models.Model):
    uid = models.IntegerField()
    employee_id = models.IntegerField()
    location_ids = models.JSONField(default=list, blank=True)
    department_id = models.IntegerField()
    user_context = models.JSONField()
    company_id = models.IntegerField()
    allowed_companies = models.JSONField()
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    def __str__(self):
        return f"TokenData(uid={self.uid})"
