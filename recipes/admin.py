from django.contrib import admin
from .models import Recipe, Comment, Saves


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ['approval_status']
    list_display = ('title', 'publish_request', 'approval_status', 'created_on')
    actions = ['approve_recipe']
    def approve_recipe(self, request, queryset):
        queryset.update(approval_status='2')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'recipe', 'created_on', 'approved')
    list_filter = ('approved', 'recipe', 'created_on')
    search_fields = ['name', 'body']
    actions = ['approve_comments']
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Saves)
class SavesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'saved_on')
    list_filter = ('recipe', 'user', 'saved_on')
