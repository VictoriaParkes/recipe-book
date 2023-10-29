from . import views
from django.urls import path
from .views import home


urlpatterns = [
    path('', home, name='home'),
    path('create_recipe', views.CreateRecipe.as_view(), name='create_recipe'),
    path('browse', views.Browse.as_view(), name='browse'),
    path('tags/<slug:tag_slug>', views.TagBrowse.as_view(), name='recipes_by_tag'),
    path('my_recipe_book', views.MyRecipeBook.as_view(), name='my_recipe_book'),
    path('<slug:slug>', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    path('save/<slug:slug>', views.RecipeSave.as_view(), name='recipe_save'),
    path('edit/<slug:slug>', views.EditRecipe.as_view(), name='recipe_edit'),
    path('delete/<slug:slug>', views.DeleteRecipe.as_view(), name='recipe_delete'),
]
