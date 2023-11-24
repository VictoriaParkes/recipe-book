from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, Comment, Saves
from django.contrib.auth.models import User


class TestHomeView(TestCase, Client):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context_data['page_title'], 'Home')


class TestRecipeListView(TestCase, Client):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('Name', '', 'password')

        Recipe.objects.create(
            title='test1',
            author_id=1,
            cooking_time=1,
            serves=1,
            ingredients=[{
                'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}
            }],
            method=[{'method': 'step 1'}],
            publish_request=True,
            approval_status=2,
        )
        Recipe.objects.create(
            title='test2',
            author_id=1,
            cooking_time=1,
            serves=1,
            ingredients=[{
                'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}
            }],
            method=[{'method': 'step 1'}],
            publish_request=False,
            approval_status=0,
        )
        Recipe.objects.create(
            title='test3',
            author_id=1,
            cooking_time=1,
            serves=1,
            ingredients=[{
                'ingredients': {'ingredient': 'bread', 'amount': '2 slices'}
            }],
            method=[{'method': 'step 1'}],
            publish_request=True,
            approval_status=1,
        )

    def test_get_browse_page(self):
        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse.html')
        self.assertEqual(response.context['page_title'], 'Browse Recipes')

    def test_browse_queryset(self):
        test_recipe_1 = Recipe.objects.get(pk=1)

        expected_qs = map(repr, [test_recipe_1])
        test_qs = Recipe.objects.filter(
            publish_request=True,
            approval_status=2
        ).order_by('-created_on')
        self.assertQuerysetEqual(test_qs, expected_qs)


class TestRecipeCreateView(TestCase, Client):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('Name', '', 'password')

    def test_not_logged_in_no_access_to_create_recipe(self):
        response = self.client.get(reverse('create_recipe'))
        self.assertRedirects(response, '/accounts/login/?next=/create_recipe')

    def test_authenticated_user_can_access_create_recipe_page(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get('/create_recipe')
        self.assertContains(response, 'title')
        self.assertContains(response, 'cooking_time')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_edit_recipe.html')
        self.assertEqual(response.context_data['page_title'], 'Create Recipe')

    def test_create_recipe(self):
        user = User.objects.get(pk=1)
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
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertRedirects(response, '/my_recipes')


class TestRecipeDetailsPage(TestCase, Client):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('Name', '', 'password')

        Recipe.objects.create(
            title='test1',
            slug='test1',
            author_id=1,
            cooking_time=1,
            serves=1,
            ingredients=('[{\"ingredients\": '
                         '{\"ingredient\": \"test\", \"amount\": \"2\"}}]'),
            method='[{\"method\": \"step 1\"}]',
            publish_request=True,
            approval_status=2,
        )

    def test_get_recipe_details_page(self):
        test_recipe_1 = Recipe.objects.get(pk=1)

        response = self.client.get(reverse(
            'recipe_detail',
            args=(test_recipe_1.slug,)
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')

    def test_post_comment(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        data = {
            'body': 'Comment',
        }
        response = self.client.post(
            '/recipe/test1',
            data=data,
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.status_code, 200)


class TestRecipeEditView(TestCase, Client):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('Author', '', 'password')
        User.objects.create_user('Name', '', 'password')

        Recipe.objects.create(
            title='test1',
            slug='test1',
            author_id=1,
            cooking_time=1,
            serves=1,
            ingredients=('[{\"ingredients\": '
                         '{\"ingredient\": \"test\", \"amount\": \"2\"}}]'),
            method='[{\"method\": \"step 1\"}]',
            publish_request=True,
            approval_status=2,
        )

    def test_not_logged_in_no_access_to_edit_recipe(self):
        response = self.client.get(reverse(
            'recipe_edit',
            kwargs={'slug': 'test1'}
        ))
        self.assertRedirects(response, '/accounts/login/?next=/edit/test1')

    def test_user_not_author_redirect(self):
        user = User.objects.get(pk=2)
        self.client.force_login(user=user)
        response = self.client.get(reverse(
            'recipe_edit',
            kwargs={'slug': 'test1'}
        ))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_recipe_author_can_access_edit_recipe_page(self):
        author = User.objects.get(pk=1)
        self.client.force_login(user=author)
        response = self.client.get(reverse(
            'recipe_edit',
            kwargs={'slug': 'test1'}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_edit_recipe.html')
