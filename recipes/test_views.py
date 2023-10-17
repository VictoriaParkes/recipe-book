from django.test import TestCase, Client
from django.urls import reverse
# from .models import *
from django.contrib.auth.models import User


class TestViews(TestCase, Client):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_get_browse_page(self):
        response = self.client.get('/browse')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse.html')

    def test_not_logged_in_no_access_to_create_recipe(self):
        response = self.client.get(reverse('create_recipe'))
        self.assertRedirects(response, '/accounts/login/?next=/create_recipe/')

    def test_authenticated_user_can_access_create_recipe_page(self):
        user = User.objects.create_user('Name', '', 'password')
        self.client.force_login(user=user)
        response = self.client.get('/create_recipe')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe.html')
