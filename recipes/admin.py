from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['approval_status']
    list_display = ('title', 'publish_request', 'approval_status', 'created_on')
