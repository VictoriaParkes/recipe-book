from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.views.generic import ListView
from django.views.generic.edit import CreateView  #, UpdateView
from .models import Recipe
from .forms import RecipeDetailsForm, IngredientsFormset, MethodFormset
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required
import json

def home(request):

    template = 'index.html'
    context = {
        'page_title': 'Home'
    }

    return render(request, template, context)

class Browse(ListView):
    model = Recipe
    queryset = Recipe.objects.filter(publish_request=True, approval_status=2).order_by('-created_on')
    template_name = 'browse.html'
    paginate_by = 12

class CreateRecipe(LoginRequiredMixin, CreateView):
    """
    Recipe Add View
    """
    model = Recipe
    form_class = RecipeDetailsForm
    template_name = 'create_recipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients_formset'] = IngredientsFormset(self.request.POST, prefix='ingredients')
            context['method_formset'] = MethodFormset(self.request.POST, prefix='method')
        else:
            context['ingredients_formset'] = IngredientsFormset(prefix='ingredients')
            context['method_formset'] = MethodFormset(prefix='method')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients_formset = context['ingredients_formset']
        method_formset = context['method_formset']

        if ingredients_formset.is_valid() and method_formset.is_valid():
            ingredients_input = ingredients_formset.cleaned_data
            ingredients_json = json.dumps(ingredients_input)
            method_input = method_formset.cleaned_data
            method_json = json.dumps(method_input)
            form.instance.author = self.request.user
            form.instance.ingredients = ingredients_json
            form.instance.method = method_json
            if form.instance.publish_request:
                form.instance.approval_status = 1
                messages.success(self.request, 'Recipe Successfully Created and Awaiting Approval')
            else:
                messages.success(self.request, 'Recipe Successfully Created')
            return super().form_valid(form)
