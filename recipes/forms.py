from django import forms
from django.forms import (
    Form,
    ModelForm,
    MultiWidget,
    MultiValueField,
    TextInput,
    Textarea,
    SelectMultiple,
    formset_factory
)
from . import models
from .models import Recipe, Comment

class RecipeDetailsForm(ModelForm):
    '''
    Form class for create recipe form without ingredients or method fields.
    '''
    class Meta:
        model = Recipe
        fields = ['title', 'recipe_image', 'tags', 'description', 'cooking_time', 'serves', 'publish_request']
        labels = {
            'publish_request': 'Make Public'
        }
        widgets = {
            'title': forms.TextInput(attrs={'max_length': 200, 'placeholder': 'Enter recipe title'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter a description of your recipe'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class IngredientsWidget(MultiWidget, TextInput):
    '''
    A widget that is composed of multiple widgets.
    '''
    def __init__(self):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'Enter Ingredient', 'required': True}),
            forms.TextInput(attrs={'placeholder': 'Enter Amount', 'required': True})
        ]
        super().__init__(widgets)

    # define how to extract values from data to be displayed in the widget.
    def decompress(self, value):
        if value:
            return [value['ingredient'], value['amount']]
        return ['', '']
    
class IngredientsField(MultiValueField):
    '''
    Define the ingredients field properties that uses the above multiwidget.
    '''
    widget = IngredientsWidget()

    def __init__(self, **kwargs):
        fields = [
            forms.CharField(max_length=50, help_text="A valid email address, please."),
            forms.CharField(max_length=50),
        ]
        super().__init__(fields=fields, **kwargs)

    # define how to process the values provided into a single piece of data.
    def compress(self, data_list):
        ingredients_dict = dict(ingredient = data_list[0], amount = data_list[1])
        return ingredients_dict

class IngredientsForm(Form):
    '''
    Form class for ingredients form.
    '''
    ingredients = IngredientsField(label='', help_text='Enter an ingredient and amount or remove empty fields.')

class MethodForm(Form):
    '''
    Form class for method form.
    '''
    method = forms.CharField(
        label='',
        help_text='Enter method step or remove empty fields.',
        widget=Textarea(attrs={'placeholder': 'Enter method step', 'rows': '3', 'required': True})
    )

# Create formset class to add multiple of the same form
IngredientsFormset = formset_factory(IngredientsForm)

MethodFormset = formset_factory(MethodForm)

class CommentForm(forms.ModelForm):
    '''
    Form class for comment form.
    '''
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,}),
        }
        labels = {
            'body': 'Add a comment'
        }
