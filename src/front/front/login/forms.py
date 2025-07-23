
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth import authenticate
from front.login.models import Shortcut


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

class RemoteBaseForm(forms.BaseForm):

    @classmethod
    def form_field_widget_override(cls, field_type, field_options, field_instance, field_name):
        readonly = field_options.get('readonly')
        # required = field_options.get('required', True)
        widget_attrs = {}

        if readonly is True:
            field_instance.widget.attrs['readonly'] = 'readonly'

        # field_instance.widget.attrs['placeholder'] = field_options.get('label')
        hidden = field_options.get('hidden')

        if hidden is True:
            field_instance.widget = forms.HiddenInput()

        field_type = field_options.get('title')

        if field_type == "TextField":
            field_instance.widget = forms.Textarea()

        field_instance.widget.attrs.update(widget_attrs)

        if isinstance(field_instance, forms.DateField):
            # field_instance.widget = CalendarWidget(data={'placeholder': field_options.get('label')})
            if hidden is False:
                field_instance.widget = CalendarWidget()

        if field_options.get("max_length", False):
            field_instance.widget.attrs.update({'data-rule-maxlength': field_options.get("max_length")})

        field_instance.widget.attrs['class'] = 'form-control '

        field_instance.error_messages.update({
            "required": "Энэ талбарыг бөглөх шаардлагатай.",
        })

        # if required is True:
        #     field_instance.widget.attrs['class'] += "required "

        return field_instance

    @classmethod
    def get_form_data_remote_url(cls):
        return "/formdatas/"

    @classmethod
    def form_field_class_override(cls, field_class, form_key, field_name, **kwargs):
        field = field_class(**kwargs)
        return field

    @classmethod
    def generate_remote_form(cls, api_post_method, company_key):
        form_key    = cls.Nova.remote_form_key
        widgets     = cls.Nova.widgets if hasattr(cls.Nova, 'widgets') else None
        labels      = cls.Nova.labels if hasattr(cls.Nova, 'labels') else None
        help_texts  = cls.Nova.help_texts if hasattr(cls.Nova, 'help_texts') else None
        widget_attrs    = cls.Nova.widget_attrs if hasattr(cls.Nova, 'widget_attrs') else None

        ALL_FIELDS_KEY = "*"

        form_operation = True
        if hasattr(cls, "_form_data") is True:
            formdata = cls._form_data
        else:
            api_res = api_post_method(
                cls.get_form_data_remote_url(),
                datas={"hdr": {"key": form_key}}
            )
            # api_response_checker(api_res, cls.get_form_data_remote_url())

            if api_result_checker(api_res) is False:
                # TODO: Reveiw
                raise Exception(str(api_res.get("msg")['body']))
            if isinstance(api_res["ret"], dict):
                formdata = api_res["ret"].get(form_key)
            elif isinstance(api_res["ret"], str) is True and api_res["ret"] == "MODULE_REQUIRED":
                formdata = {}
                form_operation = False

        fields = formdata.get('fields', [])
        properties = OrderedDict()

        # FORMDATA дээр тодорхойлсон талбарууд
        for field_name, orig_options in fields:
            options = orig_options.copy()
            field_type = options.pop('formfield')
            resource_key = options.pop('resource_key', False)
            kwargs = {}
            field_class = getattr(forms, field_type)

            if field_class == forms.IntegerField:
                field_class = NovaIntegerField

            if field_class == forms.DecimalField:
                field_class = NovaDecimalField
                kwargs['max_digits'] = 28
                kwargs['decimal_places'] = 8

            if field_class == forms.ModelChoiceField:
                field_class = forms.TypedChoiceField

            label = options.get('label')
            required = options.get('required', True)

            kwargs['label']     = label
            kwargs['required']  = required

            if isinstance(resource_key, str):
                if field_type == "ModelMultipleChoiceField":
                    field_class = MultiResourceField
                else:
                    field_class = ResourceField
                kwargs["api_post_method"] = api_post_method

                kwargs["resource_key"] = resource_key
                kwargs["resource_cache_key"] = "%s|%s" % (company_key, resource_key)

            # field = field_class(**kwargs)
            field = cls.form_field_class_override(field_class, form_key, field_name, **kwargs)

            max_length = options.get('max_length')
            if max_length:
                field.max_length = max_length
            help_text = options.get('help_text')
            if help_text:
                field.help_text = help_text

            # Widget
            field = cls.form_field_widget_override(
                field_type=field_type,
                field_options=options,
                field_instance=field,
                field_name=field_name
            )

            properties[field_name] = field

        # Override Form Fields Class
        for key, attr in cls.__dict__.items():
            if isinstance(attr, forms.Field):
                properties[key]  = attr

        for field_name in properties:
            if widgets and type(properties[field_name]) in widgets:
                properties[field_name].widget = widgets[type(properties[field_name])]
            # Nova классд зарласан widgets дотор байвал widget-ийг тодорхойлно
            if widgets and field_name in widgets:
                properties[field_name].widget = widgets[field_name]

            # Nova классд зарласан labels дотор байвал label-ийг тодорхойлно
            if labels and field_name in labels:
                properties[field_name].label = labels[field_name]

            # Nova классд зарласан help_texts дотор байвал help_text-ийг тодорхойлно
            if help_texts and field_name in help_texts:
                properties[field_name].help_text = help_texts[field_name]

            # override_widget_attrs дээр тодорхойлсон attribute-уудыг тодорхойлно (Бүх attributes ийг дарна.)
            # Жнь override_widget_attrs = {"*" : {"class" : "controler"}}
            # бүх талбарын классыг controler-р дарна required, form-control нтрийг бүгдийг дарна
            if widget_attrs and field_name in widget_attrs:
                for attr_name, attr_value in widget_attrs[field_name].items():
                    properties[field_name].widget.attrs[attr_name] = attr_value
            elif widget_attrs and ALL_FIELDS_KEY in widget_attrs:
                for attr_name, attr_value in widget_attrs[ALL_FIELDS_KEY].items():
                    properties[field_name].widget.attrs[attr_name] = attr_value

            if 'class' not in properties[field_name].widget.attrs:
                # filed-ийг дахин тодорхойлсон гэсэн үг. Default class уудыг set хийх
                properties[field_name].widget.attrs.update({'class': 'form-control'})

            if properties[field_name].required is True:
                if properties[field_name].widget.attrs.get('class', None):
                    properties[field_name].widget.attrs['class'] += ' required'

        attrs = {'base_fields': properties, }
        field_keys = properties.keys()

        # Дамжуулах шаардлагатай function уудыг дамжуулах
        req_func_lst = [
            "__init__",
            "clean",
            "declared_fields",
        ]

        methods_list = [method for method in dir(cls) if callable(getattr(cls, method)) and not method.startswith('_')]

        for method in methods_list:
            if method not in req_func_lst:
                req_func_lst.append(method)

        for field_key in field_keys:
            clean_function_name = "clean_%s" % field_key
            req_func_lst.append(clean_function_name)

        for fn_name in set(req_func_lst):
            if fn_name in cls.__dict__:
                attrs[fn_name] = cls.__dict__.get(fn_name)
        attrs["company_key"] = company_key
        attrs["form_operation"] = form_operation
        form_class  = type(form_key, (cls, forms.BaseForm,), attrs)

        return form_class


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
