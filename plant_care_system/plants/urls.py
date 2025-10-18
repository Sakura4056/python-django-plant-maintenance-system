# plant_care_system/plants/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantCategoryViewSet, PlantViewSet

router = DefaultRouter()
router.register(r'categories', PlantCategoryViewSet)
router.register(r'', PlantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]