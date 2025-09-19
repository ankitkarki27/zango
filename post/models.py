from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    artist= models.CharField(max_length=500,blank=True,null=True)
    url = models.URLField(max_length=500,blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    caption = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    
    tags = models.ManyToManyField('Tag')
   
    created_at = models.DateTimeField(auto_now_add=True)
    # uuid universal unique identifier
    id=models.CharField(max_length=100,default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    # def clean(self):
    #     """ atlaest a tag is needed for post validation"""
    #     if not self.tags.exists():
    #         raise ValidationError('Please select at least one tag.')
        
    def __str__(self):
        return str(self.caption)
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug= models.SlugField(max_length=20, unique=True)
    
    def __str__(self):
        return str(self.name)