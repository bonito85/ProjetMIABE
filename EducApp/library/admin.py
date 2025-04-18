from django.contrib import admin

from .models import Category, Ressource

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Ressource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'resource_type', 'publication_date', 'created_at')
    list_filter = ('resource_type', 'categories', 'publication_date')
    search_fields = ('title', 'description', 'author')
    filter_horizontal = ('categories',)
    date_hierarchy = 'publication_date'