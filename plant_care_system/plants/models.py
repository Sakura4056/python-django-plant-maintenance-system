# plant_care_system/plants/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class PlantCategory(models.Model):
    """Plant category model"""
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='children', verbose_name=_('Parent Category'))
    icon = models.ImageField(_('Icon'), upload_to='category_icons/', blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Plant Category')
        verbose_name_plural = _('Plant Categories')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return self.name


class Plant(models.Model):
    """Plant information model"""
    DIFFICULTY_LEVELS = (
        ('easy', _('Easy')),
        ('medium', _('Medium')),
        ('hard', _('Hard')),
    )
    
    LIGHT_REQUIREMENTS = (
        ('high', _('High Light')),
        ('medium', _('Medium Light')),
        ('low', _('Low Light')),
    )
    
    WATER_FREQUENCIES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('biweekly', _('Biweekly')),
        ('monthly', _('Monthly')),
    )

    name = models.CharField(_('Common Name'), max_length=100)
    scientific_name = models.CharField(_('Scientific Name'), max_length=200, blank=True, null=True)
    category = models.ForeignKey(PlantCategory, on_delete=models.CASCADE, 
                                related_name='plants', verbose_name=_('Category'))
    description = models.TextField(_('Description'))
    light_requirement = models.CharField(_('Light Requirement'), max_length=20, 
                                        choices=LIGHT_REQUIREMENTS, default='medium')
    water_frequency = models.CharField(_('Water Frequency'), max_length=20, 
                                      choices=WATER_FREQUENCIES, default='weekly')
    temperature_range = models.CharField(_('Temperature Range'), max_length=100, 
                                       help_text=_('e.g., 15-25°C'))
    humidity_requirement = models.CharField(_('Humidity Requirement'), max_length=50, 
                                          help_text=_('e.g., 40-60%'))
    difficulty_level = models.CharField(_('Difficulty Level'), max_length=20, 
                                      choices=DIFFICULTY_LEVELS, default='medium')
    growth_rate = models.CharField(_('Growth Rate'), max_length=50, blank=True, null=True)
    mature_size = models.CharField(_('Mature Size'), max_length=100, blank=True, null=True)
    blooming_season = models.CharField(_('Blooming Season'), max_length=100, blank=True, null=True)
    toxicity = models.CharField(_('Toxicity'), max_length=100, blank=True, null=True)
    image = models.ImageField(_('Main Image'), upload_to='plants/', blank=True, null=True)
    care_tips = models.TextField(_('Care Tips'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Plant')
        verbose_name_plural = _('Plants')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['scientific_name']),
            models.Index(fields=['category']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['light_requirement']),
        ]

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        """Return full plant name with scientific name if available"""
        if self.scientific_name:
            return f"{self.name} ({self.scientific_name})"
        return self.name