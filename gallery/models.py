from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Album model for organizing photos
class Album(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.owner.username}"
    
    def get_photo_count(self):
        return self.photos.count()


# Photo model (renamed from RecipePhoto)
class Photo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.album.name}"