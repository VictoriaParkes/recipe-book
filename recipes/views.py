from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
# from django.views.generic import ListView
from django.views.generic.edit import CreateView  #, UpdateView
from .models import Recipe
from .forms import RecipeDetailsForm, IngredientsFormset, MethodFormset, RequestPublish
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):

    template = 'index.html'
    context = {
        'page_title': 'Home'
    }

    return render(request, template, context)


class CreateRecipe(CreateView):

    def get(self, request):

        return render(
            request,
            'create_recipe.html',
            {
                'page_title': 'Create Recipe',
                'recipe_details_form': RecipeDetailsForm(prefix='details'),
                'ingredients_formset': IngredientsFormset(prefix='ingredients'),
                'method_formset': MethodFormset(prefix='method'),
                'request_publish': RequestPublish(prefix='request')
            },
        )
