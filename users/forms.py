from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','user_name')

    def clean_email(self):
        """check if the email already exists"""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('email already exists')
        return email

    def clean_user_name(self):
        """check if the email already exists"""
        user_name = self.cleaned_data.get('user_name')
        qs = User.objects.filter(user_name=user_name)
        if qs.exists():
            raise ValidationError('user_name already exists')
        return user_name

    def clean_confirm_password(self):
        """check if the both passwords match"""
        password1 = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError('passwords don\'t match')
        return confirm_password


class AdminUserCreationForm(forms.ModelForm):
    """form for creating new admin users with all fields and repeated password field"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','user_name', 'password1', 'confirm_password')

    def clean_email(self):
        """check if the email already exists"""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('email already exists')
        return email

    def clean_confirm_password(self):
        """check if the both passwords match"""
        password1 = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError('passwords don\'t match')
        return confirm_password

    def save(self, commit=False):
        """save the password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """a form for updating users including all the fields but hashed password field"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'user_name','password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]