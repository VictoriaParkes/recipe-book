from . import views
from django.urls import path


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('create_recipe', views.CreateRecipe.as_view(), name='create_recipe'),
    path('browse', views.Browse.as_view(), name='browse'),
    path('tags/<slug:tag_slug>', views.TagBrowse.as_view(), name='recipes_by_tag'),
    path('saved_recipes', views.SavedRecipes.as_view(), name='saved_recipes'),
    path('my_recipes', views.MyRecipes.as_view(), name='my_recipes'),
    path('<slug:slug>', views.RecipeDetail.as_view(), name='recipe_detail'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
    path('save/<slug:slug>', views.RecipeSave.as_view(), name='recipe_save'),
    path('edit/<slug:slug>', views.EditRecipe.as_view(), name='recipe_edit'),
    path('delete/<slug:slug>', views.DeleteRecipe.as_view(), name='recipe_delete'),
]
