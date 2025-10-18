# plant_care_system/growth/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from care.models import MyPlant


class GrowthPhoto(models.Model):
    """Model for growth photos"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='growth_photos', verbose_name=_('User'))
    my_plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, 
                               related_name='growth_photos', verbose_name=_('My Plant'))
    photo = models.ImageField(_('Photo'), upload_to='growth_photos/')
    caption = models.CharField(_('Caption'), max_length=200, blank=True, null=True)
    taken_date = models.DateTimeField(_('Taken Date'))
    height = models.FloatField(_('Height (cm)'), blank=True, null=True)
    leaf_count = models.IntegerField(_('Leaf Count'), blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Growth Photo')
        verbose_name_plural = _('Growth Photos')
        ordering = ['-taken_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['my_plant']),
            models.Index(fields=['taken_date']),
        ]

    def __str__(self):
        return f"{self.my_plant.nickname} - {self.taken_date.strftime('%Y-%m-%d')}"


class GrowthMeasurement(models.Model):
    """Model for growth measurements"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='growth_measurements', verbose_name=_('User'))
    my_plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, 
                               related_name='growth_measurements', verbose_name=_('My Plant'))
    measurement_date = models.DateField(_('Measurement Date'))
    height = models.FloatField(_('Height (cm)'), blank=True, null=True)
    leaf_count = models.IntegerField(_('Leaf Count'), blank=True, null=True)
    flower_count = models.IntegerField(_('Flower Count'), blank=True, null=True)
    fruit_count = models.IntegerField(_('Fruit Count'), blank=True, null=True)
    stem_diameter = models.FloatField(_('Stem Diameter (cm)'), blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Growth Measurement')
        verbose_name_plural = _('Growth Measurements')
        ordering = ['-measurement_date']
        unique_together = ['user', 'my_plant', 'measurement_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['my_plant']),
            models.Index(fields=['measurement_date']),
        ]

    def __str__(self):
        return f"{self.my_plant.nickname} - {self.measurement_date.strftime('%Y-%m-%d')}"


class GrowthAnalysis(models.Model):
    """Model for growth analysis results"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='growth_analyses', verbose_name=_('User'))
    my_plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, 
                               related_name='growth_analyses', verbose_name=_('My Plant'))
    analysis_date = models.DateTimeField(_('Analysis Date'), auto_now_add=True)
    growth_rate = models.FloatField(_('Growth Rate (cm/day)'), blank=True, null=True)
    health_score = models.IntegerField(_('Health Score (0-100)'), blank=True, null=True)
    recommendations = models.TextField(_('Recommendations'), blank=True, null=True)
    analysis_period = models.CharField(_('Analysis Period'), max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _('Growth Analysis')
        verbose_name_plural = _('Growth Analyses')
        ordering = ['-analysis_date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['my_plant']),
            models.Index(fields=['analysis_date']),
        ]

    def __str__(self):
        return f"{self.my_plant.nickname} Analysis - {self.analysis_date.strftime('%Y-%m-%d')}"