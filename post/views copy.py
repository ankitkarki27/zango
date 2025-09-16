from django.shortcuts import render,redirect
from .models import *
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
import requests

def home_view(request):
    # title = 'Zango here'
    posts=Post.objects.all().order_by('-created_at')
    return render(request, 'post/home.html', {'posts': posts})

class PostCreateForm(ModelForm):
    class Meta:
        model=Post
        fields=['url','caption','description']
        labels ={
            'url': 'URL',
            'caption': 'Caption',
            'description': 'Description',
        }
        widgets = {
            'caption': forms.TextInput(attrs={'rows':2,'placeholder': 'Enter caption here','class':'font-normal text-sm'}),
            'url': forms.TextInput(attrs={'rows':2,'placeholder': 'Enter image URL here','class':'font-normal text-sm'}),
            'description': forms.Textarea(attrs={'rows':2,'placeholder': 'Enter description here','class':'font-normal text-sm'}),
        }
        
def post_create_view(request):
    form= PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            # web crawler
            # beautiful soup
            post=form.save(commit=False)
            # establishing a connection
            website=requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            find_image=sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            # find_image=sourcecode.select('meta[content^="https://www.pinterest.com/pin/"]')
            image=find_image[0]['content'] if find_image else None
            post.image=image
            
            
            find_title=sourcecode.select('h1.photo-title')
            title=find_title[0].text.strip() if find_title else None
            post.title=title if title else form.data['caption']
            
            find_artist=sourcecode.select('a.owner-name')
            artist=find_artist[0].text.strip() if find_artist else None
            post.artist=artist
            post.save()
            
            # form= PostCreateForm()
            return redirect('home')
            
    return render(request, 'post/post_create.html', {'form': form})

def post_delete_view(request, pk): 
    post = Post.objects.get(id=pk)
    if request.method == "POST":  # confirm delete
        post.delete()
        return redirect('home')   # redirect back to home after deleting

    return render(request, 'post/post_delete.html', {'post': post})