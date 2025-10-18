# plant_care_system/growth/admin.py
from django.contrib import admin
from .models import GrowthPhoto, GrowthMeasurement, GrowthAnalysis


@admin.register(GrowthPhoto)
class GrowthPhotoAdmin(admin.ModelAdmin):
    list_display = ('my_plant', 'taken_date', 'user', 'caption')
    list_filter = ('taken_date', 'created_at')
    search_fields = ('my_plant__nickname', 'user__username', 'caption', 'notes')
    date_hierarchy = 'taken_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GrowthMeasurement)
class GrowthMeasurementAdmin(admin.ModelAdmin):
    list_display = ('my_plant', 'measurement_date', 'height', 'leaf_count', 'user')
    list_filter = ('measurement_date', 'created_at')
    search_fields = ('my_plant__nickname', 'user__username', 'notes')
    date_hierarchy = 'measurement_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GrowthAnalysis)
class GrowthAnalysisAdmin(admin.ModelAdmin):
    list_display = ('my_plant', 'analysis_date', 'growth_rate', 'health_score', 'user')
    list_filter = ('analysis_date',)
    search_fields = ('my_plant__nickname', 'user__username', 'recommendations')
    date_hierarchy = 'analysis_date'
    readonly_fields = ('analysis_date',)