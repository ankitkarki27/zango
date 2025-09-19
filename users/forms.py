from .models import *
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']  # Exclude the user field to prevent editing
        labels = {
            'realname': 'Full Name',
            'displayname': 'username',
            }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'image': forms.FileInput()
        }