# plant_care_system/care/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MyPlantViewSet, CarePlanViewSet, CareRecordViewSet,
    CareReminderViewSet, CareDashboardView
)

router = DefaultRouter()
router.register(r'my-plants', MyPlantViewSet)
router.register(r'care-plans', CarePlanViewSet)
router.register(r'care-records', CareRecordViewSet)
router.register(r'care-reminders', CareReminderViewSet)
router.register(r'dashboard', CareDashboardView, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]