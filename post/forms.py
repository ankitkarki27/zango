from django import forms
from django.forms import ModelForm
from .models import *

class PostCreateForm(ModelForm):
    class Meta:
        model=Post
        fields=['url','caption','description','tags']
        labels ={
            'tags': 'Tags',
            'url': 'URL',
            'caption': 'Caption',
            'description': 'Description',
        }
        widgets = {
            'caption': forms.TextInput(attrs={'rows':2,'placeholder': 'Enter caption here','class':'font-normal text-sm'}),
            'url': forms.TextInput(attrs={'rows':2,'placeholder': 'Enter image URL here','class':'font-normal text-sm'}),
            'description': forms.Textarea(attrs={'rows':2,'placeholder': 'Enter description here','class':'font-normal text-sm'}),
            'tags': forms.SelectMultiple(attrs={'class':'font-normal text-sm'}),
        }
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags:
            raise forms.ValidationError("Please select at least one tag.")
        return tags
        
class PostEditForm(ModelForm):
    class Meta:
        model=Post
        fields=['caption','description','tags']
        labels ={
            # 'url': 'URL',
            'tags': 'Tags',
            'caption': 'Caption',
            'description': 'Description',
        }
        widgets = {
            'caption': forms.TextInput(attrs={'rows':2,'placeholder': 'Enter caption here','class':'font-normal text-sm'}),
            'description': forms.Textarea(attrs={'rows':2,'placeholder': 'Enter description here','class':'font-normal text-sm'}),
        
            'tags': forms.SelectMultiple(attrs={'class':'font-normal text-sm'}),
        }
    
    # def clean_tags(self):
    #     tags = self.cleaned_data.get('tags')
    #     if not tags:
    #         raise forms.ValidationError("Please select at least one tag.")
    #     return tags