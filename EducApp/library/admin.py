from django.contrib import admin

from .models import Category, Ressource

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ressource_type', 'publication_date', 'created_at')
    list_filter = ('ressource_type', 'categories', 'publication_date')
    search_fields = ('title', 'description', 'author')
    filter_horizontal = ('categories',)
    date_hierarchy = 'publication_date'