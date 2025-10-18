# plant_care_system/care/serializers.py
from rest_framework import serializers
from .models import MyPlant, CarePlan, CareRecord, CareReminder
from plants.serializers import PlantListSerializer


class MyPlantSerializer(serializers.ModelSerializer):
    """Serializer for MyPlant model"""
    plant_details = PlantListSerializer(source='plant', read_only=True)
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    category_name = serializers.CharField(source='plant.category.name', read_only=True)
    
    class Meta:
        model = MyPlant
        fields = [
            'id', 'plant', 'plant_details', 'plant_name', 'category_name',
            'nickname', 'purchase_date', 'location', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MyPlantCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating MyPlant"""
    
    class Meta:
        model = MyPlant
        fields = ['plant', 'nickname', 'purchase_date', 'location', 'status', 'notes']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CarePlanSerializer(serializers.ModelSerializer):
    """Serializer for CarePlan model"""
    my_plant_name = serializers.CharField(source='my_plant.nickname', read_only=True)
    
    class Meta:
        model = CarePlan
        fields = [
            'id', 'my_plant', 'my_plant_name', 'plan_name',
            'water_frequency_days', 'fertilize_frequency_days', 'prune_frequency_days',
            'next_water_date', 'next_fertilize_date', 'next_prune_date',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CarePlanCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating CarePlan"""
    
    class Meta:
        model = CarePlan
        fields = [
            'my_plant', 'plan_name', 'water_frequency_days', 
            'fertilize_frequency_days', 'prune_frequency_days'
        ]
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CareRecordSerializer(serializers.ModelSerializer):
    """Serializer for CareRecord model"""
    my_plant_name = serializers.CharField(source='my_plant.nickname', read_only=True)
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)
    
    class Meta:
        model = CareRecord
        fields = [
            'id', 'my_plant', 'my_plant_name', 'record_type', 'record_type_display',
            'record_time', 'description', 'amount', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CareRecordCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating CareRecord"""
    
    class Meta:
        model = CareRecord
        fields = ['my_plant', 'record_type', 'record_time', 'description', 'amount', 'notes']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CareReminderSerializer(serializers.ModelSerializer):
    """Serializer for CareReminder model"""
    my_plant_name = serializers.CharField(source='my_plant.nickname', read_only=True)
    reminder_type_display = serializers.CharField(source='get_reminder_type_display', read_only=True)
    
    class Meta:
        model = CareReminder
        fields = [
            'id', 'my_plant', 'my_plant_name', 'care_plan',
            'reminder_type', 'reminder_type_display', 'reminder_time',
            'is_sent', 'is_completed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CareDashboardSerializer(serializers.Serializer):
    """Serializer for care dashboard statistics"""
    total_plants = serializers.IntegerField()
    healthy_plants = serializers.IntegerField()
    warning_plants = serializers.IntegerField()
    today_tasks = serializers.IntegerField()
    upcoming_tasks = serializers.IntegerField()
    recent_records = CareRecordSerializer(many=True, read_only=True)