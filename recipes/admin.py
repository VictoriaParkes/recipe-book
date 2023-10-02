from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['publish_approved']
    list_display = ('title', 'publish_request', 'publish_approved', 'created_on')
