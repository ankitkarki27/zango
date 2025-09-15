from django.db import models
import uuid
# Create your models here.
class Post(models.Model):
    image = models.URLField(max_length=500, blank=True, null=True)
    caption = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    # uuid universal unique identifier
    id=models.CharField(max_length=100,default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.caption)
        