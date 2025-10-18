# plant_care_system/plants/serializers.py
from rest_framework import serializers
from .models import PlantCategory, Plant


class PlantCategorySerializer(serializers.ModelSerializer):
    """Serializer for PlantCategory model"""
    
    class Meta:
        model = PlantCategory
        fields = ['id', 'name', 'description', 'parent', 'icon', 'created_at']


class PlantListSerializer(serializers.ModelSerializer):
    """Serializer for plant list view"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Plant
        fields = ['id', 'name', 'scientific_name', 'category_name', 
                  'difficulty_level', 'light_requirement', 'image']


class PlantDetailSerializer(serializers.ModelSerializer):
    """Serializer for plant detail view"""
    category = PlantCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=PlantCategory.objects.all(), 
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Plant
        fields = [
            'id', 'name', 'scientific_name', 'category', 'category_id',
            'description', 'light_requirement', 'water_frequency',
            'temperature_range', 'humidity_requirement', 'difficulty_level',
            'growth_rate', 'mature_size', 'blooming_season', 'toxicity',
            'image', 'care_tips', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlantCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for plant creation and update"""
    
    class Meta:
        model = Plant
        fields = [
            'name', 'scientific_name', 'category', 'description',
            'light_requirement', 'water_frequency', 'temperature_range',
            'humidity_requirement', 'difficulty_level', 'growth_rate',
            'mature_size', 'blooming_season', 'toxicity', 'image', 'care_tips'
        ]