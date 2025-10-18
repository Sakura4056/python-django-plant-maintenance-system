# plant_care_system/care/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date, timedelta
from plants.models import Plant


class MyPlant(models.Model):
    """Model for plants owned by users"""
    STATUS_CHOICES = (
        ('healthy', _('Healthy')),
        ('warning', _('Warning')),
        ('unhealthy', _('Unhealthy')),
        ('dormant', _('Dormant')),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='my_plants', verbose_name=_('User'))
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, 
                            related_name='user_plants', verbose_name=_('Plant'))
    nickname = models.CharField(_('Nickname'), max_length=100, blank=True, null=True)
    purchase_date = models.DateField(_('Purchase Date'), blank=True, null=True)
    location = models.CharField(_('Location'), max_length=100, blank=True, null=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='healthy')
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('My Plant')
        verbose_name_plural = _('My Plants')
        ordering = ['-created_at']
        unique_together = ['user', 'plant', 'nickname']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['plant']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        if self.nickname:
            return f"{self.nickname} ({self.plant.name})"
        return self.plant.name

    def save(self, *args, **kwargs):
        # Generate nickname if not provided
        if not self.nickname:
            count = MyPlant.objects.filter(user=self.user, plant=self.plant).count() + 1
            self.nickname = f"{self.plant.name} {count}"
        super().save(*args, **kwargs)


class CarePlan(models.Model):
    """Model for care plans"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='care_plans', verbose_name=_('User'))
    my_plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, 
                               related_name='care_plans', verbose_name=_('My Plant'))
    plan_name = models.CharField(_('Plan Name'), max_length=100)
    water_frequency_days = models.IntegerField(_('Water Frequency (Days)'), default=7)
    fertilize_frequency_days = models.IntegerField(_('Fertilize Frequency (Days)'), default=30)
    prune_frequency_days = models.IntegerField(_('Prune Frequency (Days)'), default=90, blank=True, null=True)
    next_water_date = models.DateField(_('Next Water Date'))
    next_fertilize_date = models.DateField(_('Next Fertilize Date'))
    next_prune_date = models.DateField(_('Next Prune Date'), blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Care Plan')
        verbose_name_plural = _('Care Plans')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['my_plant']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.plan_name} - {self.my_plant.nickname}"

    def save(self, *args, **kwargs):
        # Generate plan name if not provided
        if not self.plan_name:
            self.plan_name = f"{self.my_plant.nickname}的养护计划"
        
        # Set next care dates based on frequencies
        today = date.today()
        if not self.next_water_date:
            self.next_water_date = today + timedelta(days=self.water_frequency_days)
        if not self.next_fertilize_date:
            self.next_fertilize_date = today + timedelta(days=self.fertilize_frequency_days)
        if self.prune_frequency_days and not self.next_prune_date:
            self.next_prune_date = today + timedelta(days=self.prune_frequency_days)
        
        super().save(*args, **kwargs)


class CareRecord(models.Model):
    """Model for care records"""
    RECORD_TYPES = (
        ('water', _('Watering')),
        ('fertilize', _('Fertilizing')),
        ('prune', _('Pruning')),
        ('pest_control', _('Pest Control')),
        ('repot', _('Repotting')),
        ('clean', _('Cleaning')),
        ('other', _('Other')),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='care_records', verbose_name=_('User'))
    my_plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, 
                               related_name='care_records', verbose_name=_('My Plant'))
    record_type = models.CharField(_('Record Type'), max_length=20, choices=RECORD_TYPES)
    record_time = models.DateTimeField(_('Record Time'))
    description = models.TextField(_('Description'), blank=True, null=True)
    amount = models.CharField(_('Amount'), max_length=50, blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Care Record')
        verbose_name_plural = _('Care Records')
        ordering = ['-record_time']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['my_plant']),
            models.Index(fields=['record_type']),
            models.Index(fields=['record_time']),
        ]

    def __str__(self):
        return f"{self.get_record_type_display()} - {self.my_plant.nickname} - {self.record_time.strftime('%Y-%m-%d')}"


class CareReminder(models.Model):
    """Model for care reminders"""
    REMINDER_TYPES = (
        ('water', _('Watering Reminder')),
        ('fertilize', _('Fertilizing Reminder')),
        ('prune', _('Pruning Reminder')),
        ('repot', _('Repotting Reminder')),
        ('other', _('Other Reminder')),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='care_reminders', verbose_name=_('User'))
    my_plant = models.ForeignKey(MyPlant, on_delete=models.CASCADE, 
                               related_name='care_reminders', verbose_name=_('My Plant'))
    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, 
                                 related_name='reminders', verbose_name=_('Care Plan'), 
                                 blank=True, null=True)
    reminder_type = models.CharField(_('Reminder Type'), max_length=20, choices=REMINDER_TYPES)
    reminder_time = models.DateTimeField(_('Reminder Time'))
    is_sent = models.BooleanField(_('Is Sent'), default=False)
    is_completed = models.BooleanField(_('Is Completed'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Care Reminder')
        verbose_name_plural = _('Care Reminders')
        ordering = ['reminder_time']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['my_plant']),
            models.Index(fields=['is_sent']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['reminder_time']),
        ]

    def __str__(self):
        status = "Sent" if self.is_sent else "Pending"
        completed = "Completed" if self.is_completed else "Not Completed"
        return f"{self.get_reminder_type_display()} - {self.my_plant.nickname} - {status} - {completed}"