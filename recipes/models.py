from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField
from django_jsonform.models.fields import JSONField

# choices
# RECIPE_COURSE = (
#     ('breakfast', 'Breakfast'),
#     ('lunch', 'Lunch'),
#     ('dinner', 'Dinner'),
#     ('dessert', 'Dessert'),
#     ('supper', 'Supper'),
#     ('snack', 'Snack'),
# )

APPROVAL_STATUS = (
    ('0', 'Pending Approval'),
    ('1', 'Approved'),
    ('2', 'Rejected'),
)

# JSONField schemas
COURSE_SCHEMA = {
    'type': 'array',
    'title': 'Course',
    'items': {
            'type': 'string',
            'choices': [
                'Breakfast',
                'Lunch',
                'Dinner',
                'Dessert',
                'Supper',
                'Snack'
            ],
        'helpText': 'Select all that apply',
        'widget': 'multiselect'
    }
}

INGREDIENTS_SCHEMA = {
    'type': 'array',
    'title': 'Ingredients',
    'description': 'Add the ingredients and amount needed for your recipe',
    'items': {
            'type': 'dict',
            'keys': {
                'ingredient': {
                    'type': 'string',
                    'required': True
                },
                'amount': {
                    'type': 'string',
                    'required': True
                }
            }
    },
    'minItems': 1
}

METHOD_SCHEMA = {
    'type': 'array',
    'title': 'Method',
    'description': 'Add steps for your recipe method',
    'items': {
            'type': 'string',
            'widget': 'textarea',
            'required': True
    },
    'minItems': 1
}

# recipe model
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    recipe_image = CloudinaryField('image', default='placeholder')
    course = JSONField(schema=COURSE_SCHEMA)
    description = models.TextField(blank=True)
    ingredients = JSONField(schema=INGREDIENTS_SCHEMA)
    method = JSONField(schema=METHOD_SCHEMA)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    publish_request = models.BooleanField(default=False)
    publish_approved = models.CharField(max_length=50, choices=APPROVAL_STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
