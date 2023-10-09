from . import views
from django.urls import path, include
from .views import home, CreateRecipe

urlpatterns = [
    path('', home, name='home'),
    path('create_recipe/', views.CreateRecipe.as_view(), name='create_recipe'),
    # path('create_recipe/', CreateRecipe, name='create_recipe'),
]
