from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory, MultiWidget, MultiValueField, TextInput
from .models import Recipe

class RecipeDetailsForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'recipe_image', 'course', 'description', )
        labels = {
            'title': 'Recipe Title',
            'recipe_image': 'Image',
            'course': 'Course',
            'description': 'Recipe Description'
        }

class IngredientsWidget(MultiWidget, TextInput):
    def __init__(self):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'Enter Ingredient'}),
            forms.TextInput(attrs={'placeholder': 'Enter Amount'})
        ]
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return value.split(' ')
        return ['', '']
    
# class IngredientsField(MultiValueField):
#     widget = IngredientsWidget

#     fields = (
#         forms.CharField(),
#         forms.CharField()
#     )

#     def compress(self, input_list):
#         return ''.join(input_list)

IngredientsFormset = modelformset_factory(
    Recipe,
    fields=('ingredients', ),
    # extra=1,
    widgets={'ingredients': IngredientsWidget()}
)

MethodFormset = modelformset_factory(
    Recipe,
    fields=('method', ),
    # extra=1,
    widgets={'method': TextInput()}
)

class RequestPublish(ModelForm):
    class Meta:
        model = Recipe
        fields = ('publish_request', )
        labels = {
            'publish_request': 'Make Public'
        }