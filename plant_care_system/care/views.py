# plant_care_system/care/views.py
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import date, timedelta
from .models import MyPlant, CarePlan, CareRecord, CareReminder
from .serializers import (
    MyPlantSerializer, MyPlantCreateSerializer,
    CarePlanSerializer, CarePlanCreateSerializer,
    CareRecordSerializer, CareRecordCreateSerializer,
    CareReminderSerializer, CareDashboardSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class MyPlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user's plants.
    """
    serializer_class = MyPlantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['plant', 'status', 'location']
    search_fields = ['nickname', 'plant__name', 'plant__scientific_name', 'notes']
    ordering_fields = ['created_at', 'purchase_date', 'status']

    def get_queryset(self):
        return MyPlant.objects.filter(user=self.request.user).select_related('plant', 'plant__category')

    def get_serializer_class(self):
        if self.action == 'create':
            return MyPlantCreateSerializer
        return MyPlantSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def generate_care_plan(self, request, pk=None):
        """Generate a care plan for a specific plant"""
        my_plant = self.get_object()
        plant = my_plant.plant
        
        # Determine care frequencies based on plant characteristics
        if plant.difficulty_level == 'easy':
            water_days = 7
            fertilize_days = 30
        elif plant.difficulty_level == 'medium':
            water_days = 5
            fertilize_days = 20
        else:  # hard
            water_days = 3
            fertilize_days = 15
        
        # Adjust based on light requirement
        if plant.light_requirement == 'high':
            water_days = max(1, water_days - 2)
        elif plant.light_requirement == 'low':
            water_days += 2
        
        # Create care plan
        care_plan = CarePlan.objects.create(
            user=request.user,
            my_plant=my_plant,
            plan_name=f"{my_plant.nickname}的智能养护计划",
            water_frequency_days=water_days,
            fertilize_frequency_days=fertilize_days,
            prune_frequency_days=90
        )
        
        return Response(
            CarePlanSerializer(care_plan).data,
            status=status.HTTP_201_CREATED
        )


class CarePlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing care plans.
    """
    serializer_class = CarePlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['my_plant', 'is_active']
    search_fields = ['plan_name']
    ordering_fields = ['created_at', 'next_water_date', 'next_fertilize_date']

    def get_queryset(self):
        return CarePlan.objects.filter(user=self.request.user).select_related('my_plant')

    def get_serializer_class(self):
        if self.action == 'create':
            return CarePlanCreateSerializer
        return CarePlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CareRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing care records.
    """
    serializer_class = CareRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['my_plant', 'record_type']
    search_fields = ['description', 'notes']
    ordering_fields = ['record_time', 'created_at']

    def get_queryset(self):
        return CareRecord.objects.filter(user=self.request.user).select_related('my_plant')

    def get_serializer_class(self):
        if self.action == 'create':
            return CareRecordCreateSerializer
        return CareRecordSerializer

    def perform_create(self, serializer):
        record = serializer.save(user=self.request.user)
        
        # Update care plan next dates if needed
        if record.record_type == 'water':
            care_plans = CarePlan.objects.filter(
                user=self.request.user,
                my_plant=record.my_plant,
                is_active=True
            )
            for plan in care_plans:
                plan.next_water_date = date.today() + timedelta(days=plan.water_frequency_days)
                plan.save()
        elif record.record_type == 'fertilize':
            care_plans = CarePlan.objects.filter(
                user=self.request.user,
                my_plant=record.my_plant,
                is_active=True
            )
            for plan in care_plans:
                plan.next_fertilize_date = date.today() + timedelta(days=plan.fertilize_frequency_days)
                plan.save()
        
        return record


class CareReminderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing care reminders.
    """
    serializer_class = CareReminderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['my_plant', 'reminder_type', 'is_sent', 'is_completed']
    search_fields = ['reminder_type']
    ordering_fields = ['reminder_time', 'created_at']

    def get_queryset(self):
        return CareReminder.objects.filter(user=self.request.user).select_related('my_plant', 'care_plan')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_completed(self, request):
        """Mark a reminder as completed"""
        reminder_id = request.data.get('reminder_id')
        try:
            reminder = CareReminder.objects.get(id=reminder_id, user=request.user)
            reminder.is_completed = True
            reminder.save()
            return Response({'status': 'success'})
        except CareReminder.DoesNotExist:
            return Response({'status': 'error', 'message': 'Reminder not found'}, 
                           status=status.HTTP_404_NOT_FOUND)


class CareDashboardView(viewsets.ViewSet):
    """
    ViewSet for care dashboard statistics.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get dashboard statistics"""
        today = date.today()
        next_week = today + timedelta(days=7)
        
        # Plant statistics
        total_plants = MyPlant.objects.filter(user=request.user).count()
        healthy_plants = MyPlant.objects.filter(user=request.user, status='healthy').count()
        warning_plants = MyPlant.objects.filter(user=request.user, status='warning').count()
        
        # Task statistics
        today_tasks = CareReminder.objects.filter(
            user=request.user,
            reminder_time__date=today,
            is_completed=False
        ).count()
        
        upcoming_tasks = CareReminder.objects.filter(
            user=request.user,
            reminder_time__date__gt=today,
            reminder_time__date__lte=next_week,
            is_completed=False
        ).count()
        
        # Recent records
        recent_records = CareRecord.objects.filter(
            user=request.user
        ).order_by('-record_time')[:5]
        
        data = {
            'total_plants': total_plants,
            'healthy_plants': healthy_plants,
            'warning_plants': warning_plants,
            'today_tasks': today_tasks,
            'upcoming_tasks': upcoming_tasks,
            'recent_records': recent_records
        }
        
        serializer = CareDashboardSerializer(data)
        return Response(serializer.data)