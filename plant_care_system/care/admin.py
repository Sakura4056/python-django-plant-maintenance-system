# plant_care_system/care/admin.py
from django.contrib import admin
from .models import MyPlant, CarePlan, CareRecord, CareReminder


@admin.register(MyPlant)
class MyPlantAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'plant', 'user', 'purchase_date', 'location', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('nickname', 'plant__name', 'user__username', 'location')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CarePlan)
class CarePlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'my_plant', 'user', 'is_active', 'next_water_date', 'next_fertilize_date')
    list_filter = ('is_active', 'created_at')
    search_fields = ('plan_name', 'my_plant__nickname', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CareRecord)
class CareRecordAdmin(admin.ModelAdmin):
    list_display = ('my_plant', 'record_type', 'record_time', 'user')
    list_filter = ('record_type', 'record_time')
    search_fields = ('my_plant__nickname', 'user__username', 'description', 'notes')
    date_hierarchy = 'record_time'
    readonly_fields = ('created_at',)


@admin.register(CareReminder)
class CareReminderAdmin(admin.ModelAdmin):
    list_display = ('my_plant', 'reminder_type', 'reminder_time', 'is_sent', 'is_completed', 'user')
    list_filter = ('reminder_type', 'is_sent', 'is_completed', 'reminder_time')
    search_fields = ('my_plant__nickname', 'user__username')
    date_hierarchy = 'reminder_time'
    readonly_fields = ('created_at', 'updated_at')