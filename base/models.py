from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    """Represents different job categories available in the application"""
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Job(models.Model):
    """A model that represents Job data"""
    # TODO: add more attributes later, in accordance with a specific API
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # applicants = 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    """A class that represents comments on posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

