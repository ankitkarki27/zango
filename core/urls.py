
from django.contrib import admin
from django.urls import path
from post.views import *
from post.views import home_view,post_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('post/create/', post_create_view, name='post-create'),
]
