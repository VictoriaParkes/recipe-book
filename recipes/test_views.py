from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe
from django.contrib.auth.models import User


class TestHomeView(TestCase, Client):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class TestRecipeListView(TestCase, Client):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('Name', '', 'password')
        
        Recipe.objects.create(
            title='test1',
            author = user,
            cooking_time=1,
            serves=1,
            ingredients=[{'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}}],
            method=[{'method': 'step 1'}],
            publish_request=True,
            approval_status=2,
        )
        Recipe.objects.create(
            title='test2',
            author = user,
            cooking_time=1,
            serves=1,
            ingredients=[{'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}}],
            method=[{'method': 'step 1'}],
            publish_request=False,
            approval_status=0,
        )
        Recipe.objects.create(
            title='test3',
            author = user,
            cooking_time=1,
            serves=1,
            ingredients=[{'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}}],
            method=[{'method': 'step 1'}],
            publish_request=True,
            approval_status=1,
        )

    def test_get_browse_page(self):
        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse.html')
    
    def test_browse_queryset(self):
        test_recipe_1 = Recipe.objects.get(pk=1)

        expected_qs = map(repr, [test_recipe_1])
        test_qs = Recipe.objects.filter(publish_request=True, approval_status=2).order_by('-created_on')
        self.assertQuerysetEqual(test_qs, expected_qs)
    
class TestRecipeCreateView(TestCase, Client):

    def test_not_logged_in_no_access_to_create_recipe(self):
        response = self.client.get(reverse('create_recipe'))
        self.assertRedirects(response, '/accounts/login/?next=/create_recipe')

    def test_authenticated_user_can_access_create_recipe_page(self):
        user = User.objects.create_user('Name', '', 'password')
        self.client.force_login(user=user)
        response = self.client.get('/create_recipe')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_edit_recipe.html')

    def test_create_recipe(self):
        user = User.objects.create_user('Name', '', 'password')
        self.client.force_login(user=user)
        response = self.client.post('/create_recipe', {
            'title': 'test',
            'cooking_time': '1',
            'serves': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-TOTAL_FORMS': '2',
            'ingredients-0-ingredients_0': 'bread',
            'ingredients-0-ingredients_1': '2 slices',
            'method-INITIAL_FORMS': '0',
            'method-TOTAL_FORMS': '2',
            'method-0-method': 'step 1',
            'method-1-method': 'step 2',
        })
        self.assertRedirects(response, '/')

class TestRecipeDetailsPage(TestCase, Client):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('Name', '', 'password')
        
        Recipe.objects.create(
            title='test1',
            slug='test1',
            author = user,
            cooking_time=1,
            serves=1,
            ingredients="[{\"ingredients\": {\"ingredient\": \"test ingredient\", \"amount\": \"2 slices\"}}]",
            method="[{\"method\": \"step 1\"}]",
            publish_request=True,
            approval_status=2,
        )
        
    def test_get_recipe_details_page(self):
        test_recipe_1 = Recipe.objects.get(pk=1)

        response = self.client.get(reverse('recipe_detail', args=(test_recipe_1.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
