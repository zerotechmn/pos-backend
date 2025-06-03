
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth import authenticate
from login.models import Shortcut
from forms import RemoteBaseForm


class LoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control placeholder-no-fix"
        self.fields['password'].widget.attrs['class'] = "form-control placeholder-no-fix"
        self.fields['username'].widget.attrs['placeholder'] = u"Нэвтрэх нэр"
        self.fields['password'].widget.attrs['placeholder'] = u"Нууц үг"

    def clean_username(self, ):
        uname = self.cleaned_data.get("username")
        if uname:
            uname = uname.strip()
        return uname


class CustomerLoginForm(LoginForm):

    def __init__(self, request=None, *args, **kwargs):
        super(CustomerLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = u"Нэвтрэх код"

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Backend  ne oor backend duudaj bgaa
            self.user_cache = authenticate(usr_code=username,
                                           pin_code=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ShortcutForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShortcutForm, self).__init__(*args, **kwargs)
        self.fields['url'].widget = forms.HiddenInput()
        self.fields['com_key'].widget = forms.HiddenInput()
        self.fields['menu_key'].widget = forms.HiddenInput()
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['icon'].widget.attrs['class'] = "form-control icon_chooser"

    def get_prefix(self):
        return "shortcut"

    class Meta:
        model = Shortcut
        exclude = ["user", "user_email"]


class GlobalUserRegisterForm(RemoteBaseForm):
    """
        Бүртгүүлэх Form
    """
    accept_term = forms.BooleanField(label='Үйлчилгээний нөхцөл', required=True)

    class Nova:
        remote_form_key = 'REGISTER_STEP1_FORM'

        widget_attrs = {
            "usr_email": {"class": "form-control", "placeholder": "Имэйл хаяг"},
            "usr_ovog": {"class": "form-control", "placeholder": "Эцэг/эхийн нэр"},
            "usr_name": {"class": "form-control", "placeholder": "Нэр"},
            "phone_num": {"class": "form-control", "placeholder": "Утасны дугаар"},
            "accept_term": {"class": "accept_term", "placeholder": "Үйлчилгээний нөхцөл"},
        }


class GlobalUserComfirmForm(RemoteBaseForm):
    """
        Бүртгэл баталгаажуулах Form
    """
    class Nova:
        remote_form_key = 'REGISTER_STEP3_FORM'

        widgets = {
            "password": forms.PasswordInput(),
            "re_password": forms.PasswordInput(),
        }

        widget_attrs = {
            "password": {"class": "form-control", "placeholder": "Нууц үг"},
            "re_password": {"class": "form-control", "placeholder": "Нууц үг (давтах)"},
        }


class UserUpdateForm(RemoteBaseForm):
    """
        Хувийн мэдээлэл засах Form
    """
    class Nova:
        remote_form_key = 'USER_UPDATE_FORM'


class PasswordChangeForm(RemoteBaseForm):
    """
        Нууц үг солих Form
    """
    class Nova:
        remote_form_key = 'PASSWORD_CHANGE_FORM'

        widgets = {
            "password": forms.PasswordInput(),
            "new_password": forms.PasswordInput(),
            "re_new_password": forms.PasswordInput(),
        }

        widget_attrs = {
            "password": {"class": "form-control", "placeholder": "Нууц үг"},
            "new_password": {"class": "form-control", "placeholder": "Нууц үг (шинэ)"},
            "re_new_password": {"class": "form-control", "placeholder": "Нууц үг (давтах)"},
        }


class GlobalUserRegisterByInvitationForm(RemoteBaseForm):
    """
        Бүртгүүлэх Form
    """

    accept_term = forms.BooleanField(label='Үйлчилгээний нөхцөл', required=True)

    class Nova:
        remote_form_key = 'REGISTER_BY_INVITATION_FORM'

        widgets = {
            "password": forms.PasswordInput(),
            "re_password": forms.PasswordInput(),
        }

        widget_attrs = {
            "password": {"class": "form-control", "placeholder": "Нууц үг"},
            "re_password": {"class": "form-control", "placeholder": "Нууц үг (давтах)"},
            "accept_term": {"class": "accept_term", "placeholder": "Үйлчилгээний нөхцөл"},
        }


class PasswordResetStep1Form(RemoteBaseForm):
    """
        Нууц үгээ дахин сэргээх Form
    """
    class Nova:
        remote_form_key = 'PASSWORD_RESET_STEP1_FORM'

        widget_attrs = {
            "usr_email": {"class": "form-control", "placeholder": "Имэйл хаяг"},
        }


class PasswordResetStep3Form(RemoteBaseForm):
    """
        Нууц үгээ дахин сэргээх Form
    """
    class Nova:
        remote_form_key = 'PASSWORD_RESET_STEP3_FORM'

        widgets = {
            "password": forms.PasswordInput(),
            "re_password": forms.PasswordInput(),
        }

        widget_attrs = {
            "password": {"class": "form-control", "placeholder": "Нууц үг"},
            "re_password": {"class": "form-control", "placeholder": "Нууц үг (давтах)"},
        }


class ReferUserFilterForm(RemoteBaseForm):

    class Nova:
        remote_form_key = "B01_REFER_USER_FILTER_FORM"


class ReferToUserFormData(RemoteBaseForm):

    class Nova:
        remote_form_key = "B10_REFER_TO_USER_FORM_DATA"

        widget_attrs = {
            "message": {"class": "form-control", 'rows': '3', 'cols': '10'},
        }
