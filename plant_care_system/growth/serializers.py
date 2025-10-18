# plant_care_system/growth/serializers.py
from rest_framework import serializers
from .models import GrowthPhoto, GrowthMeasurement, GrowthAnalysis


class GrowthPhotoSerializer(serializers.ModelSerializer):
    """Serializer for GrowthPhoto model"""
    my_plant_name = serializers.CharField(source='my_plant.nickname', read_only=True)
    
    class Meta:
        model = GrowthPhoto
        fields = [
            'id', 'my_plant', 'my_plant_name', 'photo', 'caption',
            'taken_date', 'height', 'leaf_count', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GrowthPhotoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating GrowthPhoto"""
    
    class Meta:
        model = GrowthPhoto
        fields = ['my_plant', 'photo', 'caption', 'taken_date', 'height', 'leaf_count', 'notes']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GrowthMeasurementSerializer(serializers.ModelSerializer):
    """Serializer for GrowthMeasurement model"""
    my_plant_name = serializers.CharField(source='my_plant.nickname', read_only=True)
    
    class Meta:
        model = GrowthMeasurement
        fields = [
            'id', 'my_plant', 'my_plant_name', 'measurement_date',
            'height', 'leaf_count', 'flower_count', 'fruit_count',
            'stem_diameter', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GrowthMeasurementCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating GrowthMeasurement"""
    
    class Meta:
        model = GrowthMeasurement
        fields = [
            'my_plant', 'measurement_date', 'height', 'leaf_count',
            'flower_count', 'fruit_count', 'stem_diameter', 'notes'
        ]
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GrowthAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for GrowthAnalysis model"""
    my_plant_name = serializers.CharField(source='my_plant.nickname', read_only=True)
    
    class Meta:
        model = GrowthAnalysis
        fields = [
            'id', 'my_plant', 'my_plant_name', 'analysis_date',
            'growth_rate', 'health_score', 'recommendations',
            'analysis_period'
        ]
        read_only_fields = ['id', 'analysis_date']


class GrowthTimelineSerializer(serializers.Serializer):
    """Serializer for growth timeline data"""
    date = serializers.DateField()
    height = serializers.FloatField(allow_null=True)
    leaf_count = serializers.IntegerField(allow_null=True)
    photos = GrowthPhotoSerializer(many=True, read_only=True)


class GrowthStatisticsSerializer(serializers.Serializer):
    """Serializer for growth statistics"""
    average_growth_rate = serializers.FloatField()
    max_height = serializers.FloatField()
    min_height = serializers.FloatField()
    total_photos = serializers.IntegerField()
    total_measurements = serializers.IntegerField()
    health_score = serializers.IntegerField()