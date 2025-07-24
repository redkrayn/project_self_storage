from django import forms
from .models import CustomUser
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password")
        widgets = {"password": forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EmailWidget(Widget):
    def flat_att(self, attrs):
        if not attrs:
            return ""
        return "".join([' {}="{}"'.format(k, v) for k, v in attrs.items()])

    def render(self, name, value, attrs=None, renderer=None):
        attrs = {
            "class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey",
            "placeholder": "E-mail",
            "type": "email",
            "name": "email"
        }
        final_attrs = self.flat_att(attrs)
        return mark_safe(f"<input {final_attrs}>")


class PasswordWidget(Widget):
    def flat_att(self, attrs):
        if not attrs:
            return ""
        return "".join([' {}="{}"'.format(k, v) for k, v in attrs.items()])

    def render(self, name, value, attrs=None, renderer=None):
        attrs = {
            "class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey",
            "placeholder": "Password",
            "type": "text",
            "name": "password"
        }
        final_attrs = self.flat_att(attrs)
        return mark_safe(f"<input {final_attrs}>")


class LoginForm(forms.Form):
    email = forms.EmailField(label="Электронная почта", widget=EmailWidget())
    password = forms.CharField(label="Пароль", widget=PasswordWidget())
