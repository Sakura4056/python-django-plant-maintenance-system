# plant_care_system/growth/views.py
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Count
from datetime import datetime, timedelta
from .models import GrowthPhoto, GrowthMeasurement, GrowthAnalysis
from .serializers import (
    GrowthPhotoSerializer, GrowthPhotoCreateSerializer,
    GrowthMeasurementSerializer, GrowthMeasurementCreateSerializer,
    GrowthAnalysisSerializer, GrowthTimelineSerializer, GrowthStatisticsSerializer
)
from care.views import IsOwnerOrReadOnly


class GrowthPhotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing growth photos.
    """
    serializer_class = GrowthPhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['my_plant']
    search_fields = ['caption', 'notes']
    ordering_fields = ['taken_date', 'created_at']

    def get_queryset(self):
        return GrowthPhoto.objects.filter(user=self.request.user).select_related('my_plant')

    def get_serializer_class(self):
        if self.action == 'create':
            return GrowthPhotoCreateSerializer
        return GrowthPhotoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GrowthMeasurementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing growth measurements.
    """
    serializer_class = GrowthMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['my_plant']
    search_fields = ['notes']
    ordering_fields = ['measurement_date', 'created_at']

    def get_queryset(self):
        return GrowthMeasurement.objects.filter(user=self.request.user).select_related('my_plant')

    def get_serializer_class(self):
        if self.action == 'create':
            return GrowthMeasurementCreateSerializer
        return GrowthMeasurementSerializer

    def perform_create(self, serializer):
        measurement = serializer.save(user=self.request.user)
        
        # Auto-generate growth analysis if enough data exists
        self.generate_growth_analysis(measurement.my_plant)
        
        return measurement

    def generate_growth_analysis(self, my_plant):
        """Generate growth analysis based on measurements"""
        measurements = GrowthMeasurement.objects.filter(
            user=self.request.user,
            my_plant=my_plant,
            height__isnull=False
        ).order_by('measurement_date')
        
        if len(measurements) >= 2:
            # Calculate growth rate
            first = measurements.first()
            last = measurements.last()
            days = (last.measurement_date - first.measurement_date).days
            
            if days > 0:
                growth_rate = (last.height - first.height) / days
                
                # Calculate health score based on growth rate and care records
                health_score = self.calculate_health_score(my_plant, growth_rate)
                
                # Generate recommendations
                recommendations = self.generate_recommendations(my_plant, growth_rate, health_score)
                
                # Create or update analysis
                GrowthAnalysis.objects.create(
                    user=self.request.user,
                    my_plant=my_plant,
                    growth_rate=round(growth_rate, 2),
                    health_score=health_score,
                    recommendations=recommendations,
                    analysis_period=f"{first.measurement_date} to {last.measurement_date}"
                )

    def calculate_health_score(self, my_plant, growth_rate):
        """Calculate health score based on multiple factors"""
        base_score = 70
        
        # Growth rate factor (0-20 points)
        if growth_rate > 0.5:
            growth_points = 20
        elif growth_rate > 0.2:
            growth_points = 15
        elif growth_rate > 0:
            growth_points = 10
        else:
            growth_points = 5
        
        # Plant status factor (0-10 points)
        if my_plant.status == 'healthy':
            status_points = 10
        elif my_plant.status == 'warning':
            status_points = 5
        else:
            status_points = 2
        
        return min(100, base_score + growth_points + status_points)

    def generate_recommendations(self, my_plant, growth_rate, health_score):
        """Generate care recommendations based on analysis"""
        recommendations = []
        
        if growth_rate < 0.1:
            recommendations.append("植物生长缓慢，建议增加施肥频率或改善光照条件。")
        elif growth_rate > 0.5:
            recommendations.append("植物生长良好，继续保持当前养护方式。")
        
        if health_score < 60:
            recommendations.append("植物健康状况不佳，建议检查病虫害情况并调整养护方案。")
        
        if my_plant.plant.light_requirement == 'high' and '室内' in my_plant.location:
            recommendations.append("该植物需要充足光照，建议放置在阳光充足的位置。")
        
        return "\n".join(recommendations) if recommendations else "植物生长状况良好，继续保持当前养护方式。"


class GrowthAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing growth analyses.
    """
    serializer_class = GrowthAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['my_plant']
    ordering_fields = ['analysis_date']

    def get_queryset(self):
        return GrowthAnalysis.objects.filter(user=self.request.user).select_related('my_plant')


class GrowthDashboardView(viewsets.ViewSet):
    """
    ViewSet for growth dashboard data.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """Get growth timeline data for a specific plant"""
        plant_id = request.query_params.get('plant_id')
        if not plant_id:
            return Response({'error': 'plant_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            measurements = GrowthMeasurement.objects.filter(
                user=request.user,
                my_plant_id=plant_id
            ).order_by('measurement_date')
            
            photos = GrowthPhoto.objects.filter(
                user=request.user,
                my_plant_id=plant_id
            ).order_by('taken_date')
            
            # Combine measurements and photos into timeline
            timeline = []
            for measurement in measurements:
                date_photos = [p for p in photos if p.taken_date.date() == measurement.measurement_date]
                timeline.append({
                    'date': measurement.measurement_date,
                    'height': measurement.height,
                    'leaf_count': measurement.leaf_count,
                    'photos': date_photos
                })
            
            serializer = GrowthTimelineSerializer(timeline, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get growth statistics for a specific plant"""
        plant_id = request.query_params.get('plant_id')
        if not plant_id:
            return Response({'error': 'plant_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            measurements = GrowthMeasurement.objects.filter(
                user=request.user,
                my_plant_id=plant_id,
                height__isnull=False
            )
            
            if not measurements.exists():
                return Response({'error': 'No measurements found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Calculate statistics
            stats = measurements.aggregate(
                avg_height=Avg('height'),
                max_height=Max('height'),
                min_height=Min('height'),
                total=Count('id')
            )
            
            # Get latest analysis
            latest_analysis = GrowthAnalysis.objects.filter(
                user=request.user,
                my_plant_id=plant_id
            ).order_by('-analysis_date').first()
            
            # Total photos
            total_photos = GrowthPhoto.objects.filter(
                user=request.user,
                my_plant_id=plant_id
            ).count()
            
            # Calculate average growth rate
            first = measurements.order_by('measurement_date').first()
            last = measurements.order_by('measurement_date').last()
            days = (last.measurement_date - first.measurement_date).days
            avg_growth_rate = (last.height - first.height) / days if days > 0 else 0
            
            data = {
                'average_growth_rate': round(avg_growth_rate, 2),
                'max_height': stats['max_height'],
                'min_height': stats['min_height'],
                'total_photos': total_photos,
                'total_measurements': stats['total'],
                'health_score': latest_analysis.health_score if latest_analysis else 70
            }
            
            serializer = GrowthStatisticsSerializer(data)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)