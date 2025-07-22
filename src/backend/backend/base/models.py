from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.postgres.fields import JSONField

class User(AbstractUser):
    USERNAME_FIELD = "username"

    name = models.CharField(max_length=20, blank=True, null=True)
    token_password = models.CharField(max_length=100, blank=True, null=True)

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


class Terminal(models.Model):
    # AUTH_BACKENDS = "backend.auth.TerminalAuthBackend"

    name = models.CharField("Terminal Name", max_length=100)
    terminal_id = models.CharField("Terminal id", max_length=100, blank=True, null=True)

    mac_address = models.CharField("MAC Address", max_length=100, null=True, blank=True)
    ip_address = models.CharField("Hardware unique id", max_length=100, null=True, blank=True)

    guur_user = models.CharField("Guur user", max_length=1000, blank=True, null=True)
    application_version = models.PositiveIntegerField("Application version number", default=0)

    # Client info
    client_version = models.CharField("Version", max_length=50, default="")
    client_agent = models.CharField("Client OS", max_length=1000, default="", null=True, blank=True)
    client_ip = models.CharField("IP Address", max_length=100, default="", null=True, blank=True)
    ip_address = models.CharField("IP Address", max_length=100, default="", null=True, blank=True)

    class Meta:
        verbose_name = "POS Terminal"
    
    to_json_fields = [
        "name",
        "terminal_id",
        "mac_address",
        "ip_address",
        "guur_user",
        "application_version",
        "client_version",
        "client_agent",
        "client_ip",
        "ip_address",
    ]
