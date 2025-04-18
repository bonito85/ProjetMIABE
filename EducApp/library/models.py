from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Ressource(models.Model):
    RESOURCE_TYPES = (
        ('book', 'Livre'),
        ('article', 'Article'),
        ('document', 'Document'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=200)
    publication_date = models.DateField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title