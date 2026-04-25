from django.contrib import admin

from .models import DetectionHistory, TrafficSignClass, TrainingImage


@admin.register(TrafficSignClass)
class TrafficSignClassAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "meaning")


@admin.register(TrainingImage)
class TrainingImageAdmin(admin.ModelAdmin):
    list_display = ("sign_class", "created_at")
    list_filter = ("sign_class",)


@admin.register(DetectionHistory)
class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ("predicted_sign", "confidence", "created_at")
    list_filter = ("predicted_sign",)
