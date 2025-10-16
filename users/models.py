from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    displayname = models.CharField(max_length=20, blank=True, null=True)
    # realname = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    # email = models.EmailField(max_length=254, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user) 
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname or f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
        else:
            name = self.user.username
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/default_avatar.svg")
        return avatar
