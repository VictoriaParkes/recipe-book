from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

# Approval status choices
APPROVAL_STATUS = (
    ('0', 'Pending Approval'),
    ('1', 'Approved'),
    ('2', 'Rejected'),
)


# recipe model
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    recipe_image = CloudinaryField('image', default='placeholder')
    tags = TaggableManager()
    description = models.TextField(blank=True)
    ingredients = models.JSONField(null=False)
    method = models.JSONField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    publish_request = models.BooleanField(default=False)
    publish_approved = models.CharField(max_length=50, choices=APPROVAL_STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
