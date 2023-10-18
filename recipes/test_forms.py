from django.test import TestCase
from .forms import RecipeDetailsForm, IngredientsForm, MethodForm, IngredientsFormset, MethodFormset

class TestRecipeDetailsForm(TestCase):

    def test_title_is_required(self):
        form = RecipeDetailsForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')
    
    def test_cooking_time_is_required(self):
        form = RecipeDetailsForm({'title': 'test', 'cooking_time': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('cooking_time', form.errors.keys())
        self.assertEqual(form.errors['cooking_time'][0], 'This field is required.')

    def test_serves_is_required(self):
        form = RecipeDetailsForm({'title': 'test', 'cooking_time': '1', 'serves': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('serves', form.errors.keys())
        self.assertEqual(form.errors['serves'][0], 'This field is required.')
    
    def test_remaining_fields_not_required(self):
        form = RecipeDetailsForm({'title': 'test', 'cooking_time': '1', 'serves': '1'})
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = RecipeDetailsForm()
        self.assertEqual(form.Meta.fields, ['title', 'recipe_image', 'tags', 'description', 'cooking_time', 'serves', 'publish_request'])

class TestIngredientsForm(TestCase):

    def test_ingredient_is_required(self):
        form = IngredientsForm({'ingredients': {'ingredient': '', 'amount': '2 slices'}})
        self.assertFalse(form.is_valid())
        self.assertIn('ingredients', form.errors.keys())
        self.assertEqual(form.errors['ingredients'][0], 'This field is required.')
    
    def test_amount_is_required(self):
        form = IngredientsForm({'ingredients': {'ingredient': 'bread', 'amount': ''}})
        self.assertFalse(form.is_valid())
        self.assertIn('ingredients', form.errors.keys())
        self.assertEqual(form.errors['ingredients'][0], 'This field is required.')
    
    def test_ingredients_formset(self):
        data = {
            'form-INITIAL_FORMS': '0',
            'form-TOTAL_FORMS': '2',
            'form-0-ingredients_0': 'bread',
            'form-0-ingredients_1': '2 slices',
            'form-1-ingredients_0': 'ham',
            'form-1-ingredients_1': '2 slices',
        }
        formset = IngredientsFormset(data)
        self.assertTrue(formset.is_valid())
    
    # def test_ingredients_multiwidget(self):
    #     data = {
    #         'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}
    #     }
    #     widget = IngredientsWidget(data)
    #     self.assertEqual(widget.render('form-0-ingredients_0': 'bread', 'form-0-ingredients_1': '2 slices',))

class TestMethodForm(TestCase):

    def test_method_is_required(self):
        form = MethodForm({'method': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('method', form.errors.keys())
        self.assertEqual(form.errors['method'][0], 'This field is required.')
    
    def test_method_formset(self):
        data = {
            'form-INITIAL_FORMS': '0',
            'form-TOTAL_FORMS': '2',
            'form-0-method': 'step 1',
            'form-1-method': 'step 2',
        }
        formset = MethodFormset(data)
        self.assertTrue(formset.is_valid())
