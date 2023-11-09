from django.db import models
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

# Approval status choices
APPROVAL_STATUS = (
    ('0', 'Unpublished'),
    ('1', 'Pending Approval'),
    ('2', 'Approved'),
    ('3', 'Rejected'),
)

COOKING_TIME = (
    ('0', '<30 minutes'),
    ('1', '30 minutes-1 hour'),
    ('2', '1-2 hours'),
    ('3', '2-3 hours'),
    ('4', '3+ hours'),
)

# recipe model
class Recipe(models.Model):
    title = models.CharField(max_length=50, help_text= 'Required, max length 50 characters.')
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    recipe_image = CloudinaryField('image', default='placeholder')
    tags = TaggableManager(blank=True)
    description = models.TextField(max_length=300, blank=True, help_text= 'Optional, max length 300 characters.')
    cooking_time = models.CharField(max_length=50, choices=COOKING_TIME, help_text= 'Select how long your recipe takes to prepare.')
    serves = models.IntegerField(help_text= 'Enter how many people your recipes serves.')
    ingredients = models.JSONField(null=False)
    method = models.JSONField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    publish_request = models.BooleanField(default=False, help_text= 'Check this box to submit your recipe for online publication.')
    approval_status = models.CharField(max_length=50, choices=APPROVAL_STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='recipe_like', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def number_of_likes(self):
        return self.likes.count()

# comment model.
class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments'
    )
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'

# Save recipe model
class Saves(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='saves'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='save_user'
    )
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_on']
    
    def __str__(self):
        return f'Recipe saved by {self.user}'
