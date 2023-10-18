from . import views
from django.urls import path
from .views import home


urlpatterns = [
    path('', home, name='home'),
    path('create_recipe', views.CreateRecipe.as_view(), name='create_recipe'),
    path('browse', views.Browse.as_view(), name='browse'),
    path('<slug:slug>', views.RecipeDetail.as_view(), name='recipe_detail'),
]
