from django import forms
from django.forms import ModelForm
from .models import GroupMessage

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'Type a message...',
                'class': 'w-full bg-gray-700 text-white rounded-xl p-3 focus:outline-none resize-none',
                'maxlength': '500',
                'autofocus': True,
            }),
        }
