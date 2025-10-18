# plant_care_system/plants/admin.py
from django.contrib import admin
from .models import PlantCategory, Plant


@admin.register(PlantCategory)
class PlantCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'category', 'difficulty_level', 'light_requirement')
    list_filter = ('category', 'difficulty_level', 'light_requirement', 'water_frequency')
    search_fields = ('name', 'scientific_name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'scientific_name', 'category')
        }),
        ('Description', {
            'fields': ('description', 'care_tips')
        }),
        ('Growing Requirements', {
            'fields': ('light_requirement', 'water_frequency', 'temperature_range', 
                      'humidity_requirement', 'difficulty_level')
        }),
        ('Plant Characteristics', {
            'fields': ('growth_rate', 'mature_size', 'blooming_season', 'toxicity')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )