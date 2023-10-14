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
from .models import Recipe

class RecipeDetailsForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'recipe_image', 'tags', 'description', 'publish_request']
        labels = {
            'publish_request': 'Make Public'
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
            forms.CharField(max_length=50),
            forms.CharField(max_length=50),
        ]
        super().__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        ingredients_dict = dict(ingredient = data_list[0], amount = data_list[1])
        return ingredients_dict

class IngredientsForm(Form):
    ingredients = IngredientsField(label='')

class MethodForm(Form):
    method = forms.CharField(
        label='',
        widget=Textarea(attrs={'placeholder': 'Enter method step', 'required': True})
    )

IngredientsFormset = formset_factory(IngredientsForm)

MethodFormset = formset_factory(MethodForm)

# class RequestPublish(ModelForm):
#     class Meta:
#         model = Recipe
#         fields = ('publish_request', )
#         labels = {
#             'publish_request': 'Make Public'
#         }


# class RecipeAdminForm(ModelForm):
#     class Meta:
#         model = Recipe
#         widgets = {
#             'ingredients': IngredientsWidget(),
#         }
