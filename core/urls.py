
from django.contrib import admin
from django.urls import path
from post.views import *
from post.views import home_view,post_create_view,post_delete_view,post_edit_view,post_detail_view,tag_posts_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    # path('', views.home_view, name='home'),
    path('post/create/', post_create_view, name='post-create'),
    path('post/delete/<pk>/', post_delete_view, name='post-delete'),
    path('post/edit/<pk>/', post_edit_view, name='post-edit'),
    path('post/<pk>/', post_detail_view, name='post'),
    path('tag/<slug:slug>/', tag_posts_view, name='tag-posts'),

]
