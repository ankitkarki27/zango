from django.shortcuts import render,redirect
from .models import *
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .forms import PostCreateForm, PostEditForm
from django.shortcuts import get_object_or_404

# def home_view(request):
#     # title = 'Zango here'
#     posts=Post.objects.all().order_by('-created_at')
#     return render(request, 'post/home.html', {'posts': posts})

def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    tags = Tag.objects.all() 
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            url = form.cleaned_data.get('url')
            
            # Your existing URL processing logic here
            if url:
                try:
                    if "flickr.com" in url:
                        website = requests.get(url, timeout=5)
                        website.raise_for_status()
                        sourcecode = BeautifulSoup(website.text, 'html.parser')

                        find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
                        post.image = find_image[0]['content'] if find_image else None

                        find_title = sourcecode.select('h1.photo-title')
                        post.title = find_title[0].text.strip() if find_title else form.cleaned_data['caption']

                        find_artist = sourcecode.select('a.owner-name')
                        post.artist = find_artist[0].text.strip() if find_artist else None

                    elif "pinterest.com" in url:
                        website = requests.get(url, timeout=5)
                        website.raise_for_status()
                        sourcecode = BeautifulSoup(website.text, 'html.parser')

                        find_image = sourcecode.select_one('meta[property="og:image"]')
                        post.image = find_image['content'] if find_image else None

                        find_title = sourcecode.select_one('meta[property="og:title"]')
                        post.title = find_title['content'].strip() if find_title else form.cleaned_data['caption']

                        find_artist = sourcecode.select_one('meta[property="og:site_name"]')
                        post.artist = find_artist['content'].strip() if find_artist else None

                    else:
                        post.title = form.cleaned_data['caption']
                        post.image = None
                        post.artist = None

                except requests.exceptions.RequestException:
                    messages.warning(request, "Could not fetch data from the URL. Post saved without scraped image/title/artist.")
                    post.image = None
                    post.title = form.cleaned_data['caption']
                    post.artist = None
            else:
                # No URL provided
                post.title = form.cleaned_data['caption']
                post.image = None
                post.artist = None

            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
    
    return render(request, 'post/home.html', {'posts': posts, 'form': form, 'tags': tags})

def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
       
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            url = form.cleaned_data.get('url')

            if url:
                try:
                    if "flickr.com" in url:
                        website = requests.get(url, timeout=5)
                        website.raise_for_status()
                        sourcecode = BeautifulSoup(website.text, 'html.parser')

                        find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
                        post.image = find_image[0]['content'] if find_image else None

                        find_title = sourcecode.select('h1.photo-title')
                        post.title = find_title[0].text.strip() if find_title else form.cleaned_data['caption']

                        find_artist = sourcecode.select('a.owner-name')
                        post.artist = find_artist[0].text.strip() if find_artist else None

                    elif "pinterest.com" in url:
                        website = requests.get(url, timeout=5)
                        website.raise_for_status()
                        sourcecode = BeautifulSoup(website.text, 'html.parser')

                        # Pinterest often stores data in OpenGraph tags
                        find_image = sourcecode.select_one('meta[property="og:image"]')
                        post.image = find_image['content'] if find_image else None

                        find_title = sourcecode.select_one('meta[property="og:title"]')
                        post.title = find_title['content'].strip() if find_title else form.cleaned_data['caption']

                        find_artist = sourcecode.select_one('meta[property="og:site_name"]')
                        post.artist = find_artist['content'].strip() if find_artist else None

                    else:
                        # If not flickr/pinterest, just fallback
                        post.title = form.cleaned_data['caption']
                        post.image = None
                        post.artist = None

                except requests.exceptions.RequestException:
                    messages.warning(request, "Could not fetch data from the URL. Post saved without scraped image/title/artist.")
                    post.image = None
                    post.title = form.cleaned_data['caption']
                    post.artist = None
            else:
                # No URL provided
                post.title = form.cleaned_data['caption']
                post.image = None
                post.artist = None

            post.save()
            # form.save_m2m()  # Save tags
            tag_ids = request.POST.getlist('tags')
            # post.tags.set(request.POST.getlist('tags'))
            print("Selected tags:", tag_ids)  # Debug line
            # post.tags.set(tag_ids)
            if tag_ids:
                post.tags.set(tag_ids)
            # form.save_m2m()  
            messages.success(request, "Post created successfully!")
            return redirect('home')

    return render(request, 'post/post_create.html', {'form': form})


def post_delete_view(request, pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":  # confirm delete
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('home')   # redirect back to home after deleting

    return render(request, 'post/post_delete.html', {'post': post})

def post_edit_view(request, pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post)
    
    if request.method == "POST":  
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post edited successfully!")
            return redirect('home')
            # return redirect("post-detail", pk=post.pk)
    # else:
    #     form = PostEditForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }
        
    return render(request, 'post/post_edit.html', context)

def post_detail_view(request, pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    return render(request, 'post/post_detail.html', {'post': post})

def tag_posts_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tags= Tag.objects.all()
    posts = Post.objects.filter(tags=tag)
    
    context ={
        'tag': tag,
        'posts': posts,
        'tags': tags
    }
    return render(request, 'post/tag_posts.html', context)