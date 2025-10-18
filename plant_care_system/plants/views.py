# plant_care_system/plants/views.py
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import PlantCategory, Plant
from .serializers import (
    PlantCategorySerializer, PlantListSerializer, 
    PlantDetailSerializer, PlantCreateUpdateSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class PlantCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing plant categories.
    """
    queryset = PlantCategory.objects.all()
    serializer_class = PlantCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']


class PlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing plants.
    """
    queryset = Plant.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty_level', 'light_requirement', 'water_frequency']
    search_fields = ['name', 'scientific_name', 'description', 'care_tips']
    ordering_fields = ['name', 'created_at', 'difficulty_level']

    def get_serializer_class(self):
        if self.action == 'list':
            return PlantListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PlantCreateUpdateSerializer
        return PlantDetailSerializer

    def get_queryset(self):
        queryset = Plant.objects.all()
        
        # Optional filtering by search query
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                models.Q(name__icontains=search_query) |
                models.Q(scientific_name__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
        
        return queryset.select_related('category')