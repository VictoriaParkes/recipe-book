from . import views
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('create_recipe/', views.CreateRecipe.as_view(), name='create_recipe')
]
