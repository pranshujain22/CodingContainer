from django import forms
from user.models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'email', 'enrollment_id')

