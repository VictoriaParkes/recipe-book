from django.contrib import admin
from .models import Recipe, Comment, Saves


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    '''
    Register recipe model and the recipe admin class with admin site.
    '''
    # list of fields to generate filters in the right sidebar of admin panel
    list_filter = ['approval_status']
    # The fields to be displayed in the list of recipes in admin panel
    list_display = ('title', 'publish_request', 'approval_status', 'created_on')
    # Add approve recipes action
    actions = ['approve_recipe']
    # Define approve recipes action
    def approve_recipe(self, request, queryset):
        queryset.update(approval_status='2')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
    Register comment model and the comment admin class with admin site.
    '''
    list_display = ('body', 'recipe', 'created_on', 'approved')
    list_filter = ('approved', 'recipe', 'created_on')
    # search name or body of comments
    search_fields = ['name', 'body']
    actions = ['approve_comments']
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Saves)
class SavesAdmin(admin.ModelAdmin):
    '''
    Register saves model and the saves admin class with admin site.
    '''
    list_display = ('recipe', 'user', 'saved_on')
    list_filter = ('recipe', 'user', 'saved_on')
