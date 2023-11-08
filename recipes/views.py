from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Recipe, Saves, Comment
from django.db.models import Count
from .forms import RecipeDetailsForm, IngredientsFormset, MethodFormset, CommentForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import json

class Index(ListView):
    model = Recipe
    queryset = Recipe.objects.filter(publish_request=True, approval_status=2).annotate(num_likes=Count("likes")).order_by("-num_likes")[:3]
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home'
        return context

class Browse(ListView):
    model = Recipe
    queryset = Recipe.objects.filter(publish_request=True, approval_status=2).order_by('-created_on')
    template_name = 'browse.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Browse Recipes'
        return context

class TagBrowse(ListView):
    model = Recipe
    template_name = 'browse.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Browse Recipes'
        return context

    def get_queryset(self):
        return Recipe.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

class RecipeDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, slug=slug)
        page_title = recipe.title
        ingredients = json.loads(recipe.ingredients)
        method = json.loads(recipe.method)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True
        saved = False
        if request.user.is_authenticated:
            if Saves.objects.filter(recipe=recipe, user=self.request.user).exists():
                saved = True

        return render(
            request,
            'recipe_detail.html',
            {
                'recipe': recipe,
                'ingredients': ingredients,
                'method': method,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'saved': saved,
                'comment_form': CommentForm(),
                'page_title': page_title
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(publish_request=True, approval_status=2)
        recipe = get_object_or_404(queryset, slug=slug)
        page_title = recipe.title
        ingredients = json.loads(recipe.ingredients)
        method = json.loads(recipe.method)
        comments = recipe.comments.filter(approved=True).order_by('created_on')
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True
        saved = False
        if Saves.objects.filter(recipe=recipe, user=self.request.user).exists():
            saved = True
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            messages.success(request, 'Comment Successful!')
        
        return render(
            request,
            'recipe_detail.html',
            {
                'recipe': recipe,
                'ingredients': ingredients,
                'method': method,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'saved': saved,
                'comment_form': comment_form,
                'page_title': page_title
            },
        )

class RecipeLike(LoginRequiredMixin, View):
    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if recipe.likes.filter(id=self.request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)
        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))

class RecipeSave(LoginRequiredMixin, View):
    def post(self, request, slug):
        recipe_to_save = get_object_or_404(Recipe, slug=slug)
        if Saves.objects.filter(recipe=recipe_to_save, user=self.request.user).exists():
            Saves.objects.filter(recipe=recipe_to_save, user=self.request.user).delete()
        else:
            saved_recipe = Saves(recipe=recipe_to_save, user=self.request.user)
            saved_recipe.save()
        return HttpResponseRedirect(reverse('recipe_detail', args=[slug]))

class CreateRecipe(LoginRequiredMixin, CreateView):
    """
    Recipe Create View
    """
    model = Recipe
    form_class = RecipeDetailsForm
    template_name = 'create_edit_recipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients_formset'] = IngredientsFormset(self.request.POST, prefix='ingredients')
            context['method_formset'] = MethodFormset(self.request.POST, prefix='method')
            context['page_title'] = 'Create Recipe'
        else:
            context['ingredients_formset'] = IngredientsFormset(prefix='ingredients')
            context['method_formset'] = MethodFormset(prefix='method')
            context['page_title'] = 'Create Recipe'
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

class RecipeOwnerTest(UserPassesTestMixin):
    def test_func(self):
        recipe = self.get_object()
        return recipe.author == self.request.user

class EditRecipe(LoginRequiredMixin, RecipeOwnerTest, UpdateView):
    """
    Edit Recipe View
    """
    model = Recipe
    form_class = RecipeDetailsForm
    template_name = 'create_edit_recipe.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredients_formset'] = IngredientsFormset(self.request.POST, initial=json.loads(self.object.ingredients), prefix='ingredients')
            context['method_formset'] = MethodFormset(self.request.POST, initial=json.loads(self.object.method), prefix='method')
            context['page_title'] = 'Edit Recipe'
        else:
            context['ingredients_formset'] = IngredientsFormset(initial=json.loads(self.object.ingredients), prefix='ingredients')
            context['method_formset'] = MethodFormset(initial=json.loads(self.object.method), prefix='method')
            context['page_title'] = 'Edit Recipe'
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
            messages.success(self.request, 'Recipe Successfully Edited and Awaiting Approval')
        else:
            form.instance.approval_status = 0
            messages.success(self.request, 'Recipe Successfully Edited')
        return super().form_valid(form)

class DeleteRecipe(LoginRequiredMixin, RecipeOwnerTest, DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy('my_recipe_book')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Recipe'
        return context

class MyRecipeBook(LoginRequiredMixin, ListView):
    model = Saves
    template_name = 'my_recipe_book.html'
    def get_queryset(self):
        qs = super().get_queryset()
        queryset = qs.filter(user=self.request.user, recipe__publish_request=True, recipe__approval_status=2).order_by('saved_on')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_recipes_list'] = Recipe.objects.filter(author=self.request.user).order_by('-created_on')
        context['page_title'] = 'My Recipe Book'
        return context
    
def handler400(request, exception):
    """
    Custom 400 page
    """
    context = {
        'page_title': '400'
    }
    return render(request, "errors/400.html", context, status=400)

def handler403(request, exception):
    """
    Custom 403 page
    """
    context = {
        'page_title': '403'
    }
    return render(request, "errors/403.html", context, status=403)

def handler404(request, exception):
    """
    Custom 404 page
    """
    context = {
        'page_title': '404'
    }
    return render(request, "errors/404.html", context, status=404)

def handler500(request):
    """
    Custom 500 page
    """
    context = {
        'page_title': '500'
    }
    return render(request, "errors/500.html", context, status=500)
