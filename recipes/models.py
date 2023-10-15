from django.db import models
from django.contrib.auth.models import User
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

# recipe model
class Recipe(models.Model):
    title = models.CharField(max_length=200, help_text= 'Required, max length 200 characters.')
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    recipe_image = CloudinaryField('image', default='placeholder')
    tags = TaggableManager(blank=True)
    description = models.TextField(blank=True, help_text= 'Optional.')
    ingredients = models.JSONField(null=False)
    method = models.JSONField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    publish_request = models.BooleanField(default=False, help_text= 'Check this box to submit your recipe for online publication.')
    approval_status = models.CharField(max_length=50, choices=APPROVAL_STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
