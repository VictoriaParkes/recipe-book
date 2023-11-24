from django.test import TestCase, Client
from recipes.models import Recipe
from django.contrib.auth.models import User
from django.urls import reverse


class TestErrorViews(TestCase, Client):

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
    
    def test_get_404(self):

        response = self.client.get('/test')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
        self.assertEqual(response.context['page_title'], '404')

    def test_get_403(self):

        user = User.objects.get(pk=2)
        self.client.force_login(user=user)
        response = self.client.get(reverse(
            'recipe_edit',
            kwargs={'slug': 'test1'}
        ))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'errors/403.html')
        self.assertEqual(response.context['page_title'], '403')
