from django import forms
from django.forms import (
    Form,
    ModelForm,
    MultiWidget,
    MultiValueField,
    MultipleChoiceField,
    TextInput,
    SelectMultiple,
    formset_factory
)
from . import models
from .models import Recipe
from django_jsonform.widgets import JSONFormWidget


class RecipeDetailsForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'recipe_image', 'tags', 'description']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class IngredientsWidget(MultiWidget, TextInput):
    def __init__(self):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'Enter Ingredient'}),
            forms.TextInput(attrs={'placeholder': 'Enter Amount'})
        ]
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return [value['ingredient'], value['amount']]
        return ['', '']
    
class IngredientsField(MultiValueField):
    widget = IngredientsWidget()

    def __init__(self, *args, **kwargs):
        fields = [
            forms.CharField(max_length=50),
            forms.CharField(max_length=50)
        ]
        super().__init__(fields, *args, **kwargs)

    def compress(self, input_list):
        ingredients_dict = dict(ingredient = input_list[0], amount = input_list[1])
        return ingredients_dict

class IngredientsForm(Form):
    ingredients = IngredientsField(label='')

class MethodForm(Form):
    method = forms.CharField(label='', widget=TextInput(attrs={'placeholder': 'Enter method step'}))

IngredientsFormset = formset_factory(IngredientsForm)

MethodFormset = formset_factory(MethodForm)

class RequestPublish(ModelForm):
    class Meta:
        model = Recipe
        fields = ('publish_request', )
        labels = {
            'publish_request': 'Make Public'
        }



# class RecipeDetailsForm(ModelForm):
#     class Meta:
#         model = Recipe
#         fields = ('title', 'recipe_image', 'course', 'description', )
#         labels = {
#             'title': 'Recipe Title',
#             'recipe_image': 'Image',
#             'course': 'Course',
#             'description': 'Recipe Description'
#         }

# class RecipeAdminForm(ModelForm):
#     class Meta:
#         model = Recipe
#         widgets = {
#             'ingredients': IngredientsWidget(),
#         }
