from django.shortcuts import render,redirect
from .models import *
from django.forms import ModelForm
from django import forms

def home_view(request):
    # title = 'Zango here'
    posts=Post.objects.all().order_by('-created_at')
    return render(request, 'post/home.html', {'posts': posts})

class PostCreateForm(ModelForm):
    class Meta:
        model=Post
        fields='__all__'
        labels ={
            'image': 'Image URL',
            'caption': 'Caption',
            'description': 'Description',
        }
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Enter caption here','class':'font-normal text-sm'}),
            'image': forms.TextInput(attrs={'placeholder': 'Enter image URL here','class':'font-normal text-sm'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description here','class':'font-normal text-sm'}),
        }
        
def post_create_view(request):
    form= PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            form= PostCreateForm()
            return redirect('home')
            
    return render(request, 'post/post_create.html', {'form': form})
