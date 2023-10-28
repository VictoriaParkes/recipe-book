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
    def __init__(self):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'Enter Ingredient', 'required': True}),
            forms.TextInput(attrs={'placeholder': 'Enter Amount', 'required': True})
        ]
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return [value['ingredient'], value['amount']]
        return ['', '']
    
class IngredientsField(MultiValueField):
    widget = IngredientsWidget()

    def __init__(self, **kwargs):
        fields = [
            forms.CharField(max_length=50, help_text="A valid email address, please."),
            forms.CharField(max_length=50),
        ]
        super().__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        ingredients_dict = dict(ingredient = data_list[0], amount = data_list[1])
        return ingredients_dict

class IngredientsForm(Form):
    ingredients = IngredientsField(label='', help_text='Enter an ingredient and amount or remove empty fields.')

class MethodForm(Form):
    method = forms.CharField(
        label='',
        help_text='Enter method step or remove empty fields.',
        widget=Textarea(attrs={'placeholder': 'Enter method step', 'rows': '3', 'required': True})
    )

IngredientsFormset = formset_factory(IngredientsForm)

MethodFormset = formset_factory(MethodForm)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,}),
        }
        labels = {
            'body': 'Add a comment'
        }
