import datetime

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import signals

class ApiTokensManager(models.Manager):

    def safe_tokens(self):
        return self.filter(token_expire_time__gte=datetime.datetime.now())

    def find_by_token(self, token):
        return self.safe_tokens().filter(access_token=token).first()

    def find_by_email(self, email):
        return self.filter(usr_email__iexact=email).first()


class ApiUserTokens(models.Model):
    USERNAME_FIELD = "usr_email"
    REQUIRED_FIELDS = [
        "access_token",
    ]
    is_anonymous = False
    is_authenticated = True
    access_token = models.CharField(max_length=40)
    scope = models.CharField(max_length=40)
    expires_in = models.IntegerField()
    refresh_token = models.CharField(max_length=40, null=True)
    token_type = models.CharField(max_length=40)

    usr_email = models.EmailField('Имэйл', max_length=40, unique=True, null=True, blank=True)

    session_created = models.DateTimeField(auto_now_add=True)
    token_created = models.DateTimeField(default=datetime.datetime.now)
    token_expire_time = models.DateTimeField(default=datetime.datetime.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = ApiTokensManager()

    class Meta:
        verbose_name = "User Tokens"
        verbose_name_plural = "User Tokens"

    def save(self, *args, **kwargs):
        token_expire_time = self.token_created + datetime.timedelta(seconds=int(self.expires_in))
        self.token_expire_time = token_expire_time
        user_token = super(ApiUserTokens, self).save(*args, **kwargs)
        return user_token

    # TODO: Refactor
    def is_active(self):
        return True

    def __str__(self):
        return self.usr_email

    def get_user_data(self):
        if hasattr(self, "_user_data"):
            return self._user_data
        dt_now = datetime.datetime.now()
        delta = self.session_created - dt_now
        if delta.seconds > self.expires_in:
            # Refresh token
            pass
        cache_key = "USER_DATA|%s" % self.usr_email.lower()
        self._user_data = cache.get(cache_key)
        if self._user_data is None:
            self._user_data = self._user_data.get("ret")
            cache.set(cache_key, self._user_data)
        return self._user_data

    def usr_name(self):
        return self.get_user_data().get("usr_name")

    def usr_uuid(self):
        return self.get_user_data().get("pk")

    def usr_ovog(self):
        return self.get_user_data().get("usr_ovog")

    def phone_num(self):
        return self.get_user_data().get("phone_num")

    def note(self):
        return self.get_user_data().get("note")

    @property
    def usr_code(self):
        return self.get_user_data().get("usr_code")

    def get_short_name(self):
        return self.get_user_data().get("get_short_name")

    def get_avatar(self):
        return self.get_user_data().get("usr_avatar_path")

    def get_session_auth_hash(self):
        return "%s %s" % (self.token_type, self.access_token)


class ApiTokenCompanyUserManager(models.Manager):

    def safe_tokens(self):
        return self.filter(token_expire_time__gte=datetime.datetime.now())

    def find_by_token(self, token):
        return self.safe_tokens().filter(access_token=token).first()

    def find_by_usrcode(self, usr_code):
        return self.filter(usr_code__iexact=usr_code).first()


SHORTCUT_ICONS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),
    ('25', '25'),
    ('26', '26'),
    ('27', '27'),
    ('28', '28'),
    ('29', '29'),
    ('30', '30'),
    ('31', '31'),
    ('32', '32'),
    ('33', '33'),
    ('34', '34'),
    ('35', '35'),
    ('36', '36'),
    ('37', '37'),
    ('38', '38'),
    ('39', '39'),
    ('40', '40'),
    ('41', '41'),
    ('42', '42'),
    ('43', '43'),
    ('44', '44'),
    ('45', '45'),
    ('46', '46'),
    ('47', '47'),
    ('48', '48'),
    ('49', '49'),
    ('50', '50'),
    ('51', '51'),
]


class Shortcut(models.Model):
    com_key = models.CharField("Компаний нэр", max_length=200, null=True, blank=True)
    url = models.CharField("Шууд хүргэх линк", max_length=200, null=True, blank=True)
    name = models.CharField("Линкны нэр", max_length=200)
    user = models.ForeignKey(ApiUserTokens, related_name="user_shortcuts", null=True, blank=True, on_delete=models.DO_NOTHING)
    user_email = models.CharField("Хэрэглэгчийн имэйл", max_length=40, null=True, blank=True)
    icon = models.CharField("Таних тэмдэг", choices=SHORTCUT_ICONS, default='1', max_length=5)
    menu_key = models.CharField("Менүний түлхүүр", max_length=300, null=True, blank=True)
    created_date = models.DateTimeField("Үүсгэсэн огноо", auto_now_add=True)

    def get_icon_url(self):
        u"""  """
        icon = "%s" % self.icon
        return icon

    def get_icon(self):
        u""" Тэмдэглэл """
        icon = self.get_icon_url()
        return u"""<div class="shortcut%s" title ="%s"></div>""" % (icon, self.name)


def listener_login_failed(sender, credentials, **kwargs):
    uname = credentials.get("username")
    if len(uname) > 256:
        uname = uname[:256]
    # login_log(
    #     message="[%s] нэрээр нэвтрэж чадсангүй" % (uname),
    #     status=LOGIN_UNSUCCESS,
    # )

    # secure_log(
    #     reason="[%s] нэрээр нэвтрэж чадсангүй" % (uname),
    #     detail="credentials %r" % credentials,
    #     detection_source="auth",
    # )


def listener_login_success(sender, request, user, **kwargs):
    username = repr(user)
    # login_log(
    #     message="Хэрэглэгч [%s] оролдсоны дараа амжилттай логин хийв." % username,
    #     user=user,
    #     status=LOGIN_SUCCESS,
    #     request=request
    # )


def listener_logout_success(sender, request, user, **kwargs):
    username = repr(user)
    # login_log(
    #     message="Хэрэглэгч [%s] гарлаа." % username,
    #     user=user,
    #     status=LOGOUT,
    #     request=request
    # )


signals.user_logged_in.connect(listener_login_success)
signals.user_logged_out.connect(listener_logout_success)
signals.user_login_failed.connect(listener_login_failed)
