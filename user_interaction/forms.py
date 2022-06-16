from django.contrib.auth.forms import UserCreationForm
from .models import student, employer, Job
from django.forms import ModelForm
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = student
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class CreateEmployerForm(UserCreationForm):
    class Meta:
        model = employer
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class GetUserProfile(ModelForm):
    class Meta:
        model = student
        fields = ['profile']
        widgets = {
            'profile': forms.Textarea(attrs={'cols': 135, 'rows': 25})
        }


class GetJob(ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'mode_of_communication']


class OTP(forms.Form):
    otp = forms.IntegerField(label='otp', max_value=999999)
