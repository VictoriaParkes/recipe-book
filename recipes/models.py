from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField

# choices
RECIPE_COURSE = (
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('dessert', 'Dessert'),
    ('supper', 'Supper'),
    ('snack', 'Snack'),
)

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
    course = models.CharField(max_length=50, choices=RECIPE_COURSE)
    description = models.TextField(blank=True)
    ingredients = models.JSONField(null=False)
    method = models.JSONField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    publish_request = models.BooleanField(default=False)
    publish_approved = models.CharField(max_length=50, choices=APPROVAL_STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='recipe_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


# comment model
class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
