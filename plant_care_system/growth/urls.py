# plant_care_system/growth/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GrowthPhotoViewSet, GrowthMeasurementViewSet,
    GrowthAnalysisViewSet, GrowthDashboardView
)

router = DefaultRouter()
router.register(r'photos', GrowthPhotoViewSet)
router.register(r'measurements', GrowthMeasurementViewSet)
router.register(r'analyses', GrowthAnalysisViewSet)
router.register(r'dashboard', GrowthDashboardView, basename='growth-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]