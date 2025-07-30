import json
import hashlib
from django.db import models
from django.db.models import F
from django.db.models import Count
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from mongoengine import Document
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import BooleanField
from mongoengine import StringField
from mongoengine import DecimalField
from mongoengine import DateTimeField
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

class PublicIncIndexes(models.Model):
    index_key = models.CharField("Түлхүүр", unique=True, max_length=100)
    current_index = models.PositiveIntegerField("Идэвхтэй утга", default=1)

    class Meta:
        verbose_name = "Index-үүд"
        verbose_name_plural = "Index-үүд"

    @classmethod
    def get_last_index(cls, key):
        incIndex, is_index_create = cls.objects.get_or_create(index_key=key)
        current_index = 1

        if is_index_create is False:
            current_index = incIndex.current_index + 1
            incIndex.current_index = F("current_index") + 1
            incIndex.save()

            incIndex = cls.objects.get(pk=incIndex.pk)
            current_index = incIndex.current_index

        return current_index


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
    terminal_pos_no = models.CharField("Terminal id", max_length=100, blank=True, null=True)

    mac_address = models.CharField("MAC Address", max_length=100, null=True, blank=True)
    ip_address = models.CharField("Hardware unique id", max_length=100, null=True, blank=True)

    guur_user = models.CharField("Guur user", max_length=1000, blank=True, null=True)
    guur_token = models.CharField("Guur Token", max_length=1000, blank=True, null=True)

    application_version = models.CharField("Application version", max_length=1000, blank=True, null=True)

    tbd_application_version = models.CharField("TDB Application version", max_length=1000, blank=True, null=True)
    tdb_terminal_id = models.CharField("TDB Terminal number", max_length=1000, blank=True, null=True)

    pts_ip_address = models.CharField("PTS IP Address", max_length=1000, blank=True, null=True)
    
    # Client info
    client_version = models.CharField("Version", max_length=50, default="")
    client_agent = models.CharField("Client OS", max_length=1000, default="", null=True, blank=True)
    client_ip = models.CharField("IP Address", max_length=100, default="", null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.terminal_pos_no)

    class Meta:
        verbose_name = "POS Terminal"
    
    to_json_fields = [
        "name",
        "terminal_id",
        "mac_address",
        "ip_address",
        "guur_user",
        "application_version",
        "tbd_application_version",
        "tdb_terminal_id",
        
        "pts_ip_address",
    ]

class RequestLog(Document):
    remote_address = StringField(verbose_name="Request IP", max_length=10000, null=True, blank=True)

    request_action = StringField(verbose_name="Request action", max_length=10000, null=True, blank=True)
    request_url = StringField(verbose_name="Request url", max_length=10000, null=True, blank=True)
    request_date = DateTimeField(verbose_name="Request datetime", null=True, blank=True)
    request_method = StringField(verbose_name="Request method (get, post)", max_length=1000, null=True, blank=True)
    request_data = StringField(verbose_name="Request data", max_length=10000000, null=True, blank=True)
    request_headers = StringField(verbose_name="Request header", max_length=10000, null=True, blank=True)

    response_date = DateTimeField(verbose_name="Response datetime", null=True, blank=True)
    response_code = StringField(verbose_name="Response code", max_length=1000, null=True, blank=True)
    response_data = StringField(verbose_name="Response data", max_length=10000000, null=True, blank=True)
    response_status_code = StringField(verbose_name="Response status code", max_length=10000000, null=True, blank=True)

    return_data = StringField(verbose_name="Return data", max_length=10000000, null=True, bank=True)

    duration = StringField(verbose_name="Хугацаа (sec)", max_length=1000, null=True, blank=True)
    exception = StringField(verbose_name="Exception", max_length=10000000, null=True, blank=True)
    client_request_data = StringField(verbose_name="Exception", max_length=10000000, null=True, blank=True)

    terminal_id = StringField(verbose_name="Terminal UUID", max_length=1000, null=True, blank=True)
    operation_index = IntField(verbose_name="Operation index", null=True, blank=True)

    created_date = DateTimeField(verbose_name="Үүсгэсэн огноо", null=True, blank=True)
    last_updated_date = DateTimeField(verbose_name="Өөрчилсөн огноо", null=True, blank=True)

    meta = {
        'db_alias': settings.MONGODB_LOG,
        'strict': False,
        'indexes': [
            'operation_index',
            'created_date',
        ]
    }

    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

    def to_json(self):
        terminal_name = ""
        if self.terminal_id:
            terminal = Terminal.all_objects.filter(pk=self.terminal_id).first()
            if terminal:
                terminal_name = terminal.__unicode__()

        try:
            request_data = json.loads(self.request_data)
        except Exception:
            request_data = str(self.request_data)

        try:
            response_data = json.loads(self.response_data)
        except Exception:
            response_data = str(self.response_data)

        try:
            return_data = json.loads(self.return_data)
        except Exception:
            return_data = str(self.return_data)

        try:
            client_request_data = json.loads(self.client_request_data)
        except Exception:
            client_request_data = str(self.client_request_data)

        response_status_code = ""
        if self.response_status_code is not None:
            response_status_code = self.response_status_code
        elif self.response_data is not None and isinstance(response_data, dict):
            if 'status_code' in response_data:
                response_status_code = response_data['status_code']
            elif 'code' in response_data:
                response_status_code = response_data['code']

        json_data = {
            'pk': str(self.id),

            'remote_address': self.remote_address,

            'request_action': self.request_action,
            'request_url': self.request_url,
            'request_date': self.request_date.strftime("%Y-%m-%d %H:%M:%S"),
            'request_method': self.request_method,
            'request_data': request_data,

            'response_date': "" if self.response_date is None else self.response_date.strftime("%Y-%m-%d %H:%M:%S"),
            'response_code': "" if self.response_code is None else self.response_code,
            'response_data': response_data,
            'response_status_code': response_status_code,

            'return_data': return_data,

            'duration': self.duration,
            'exception': "" if self.exception is None else str(self.exception),
            'client_request_data': client_request_data,

            'terminal_name': terminal_name,
            'terminal_id': self.terminal_id,

            'operation_index': self.operation_index,

            'created_date': self.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated_date': self.last_updated_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        return json_data