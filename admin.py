from django.contrib import admin
from .models import Farm, Crop, SensorData, DiseaseReport, ResearchPaper, CompanionPlantingRule, Recommendation

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'size_acres', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'farmer__username']

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'farm', 'health_status', 'planting_date']
    list_filter = ['crop_type', 'health_status', 'planting_date']
    search_fields = ['farm__name']

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['farm', 'temperature', 'humidity', 'timestamp']
    list_filter = ['timestamp', 'farm']
    readonly_fields = ['timestamp']

@admin.register(DiseaseReport)
class DiseaseReportAdmin(admin.ModelAdmin):
    list_display = ['disease_name', 'farm', 'severity', 'verified', 'reported_at']
    list_filter = ['severity', 'verified', 'reported_at']
    search_fields = ['disease_name', 'farm__name']
    actions = ['mark_verified']
    
    def mark_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_verified.short_description = "Mark selected reports as verified"

@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'journal', 'publication_date', 'citation_count']
    list_filter = ['publication_date', 'journal']
    search_fields = ['title', 'authors', 'keywords']

@admin.register(CompanionPlantingRule)
class CompanionPlantingRuleAdmin(admin.ModelAdmin):
    list_display = ['primary_crop', 'companion_crop', 'relationship_type', 'confidence_score']
    list_filter = ['relationship_type', 'primary_crop']

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'farm', 'recommendation_type', 'confidence_score', 'implemented']
    list_filter = ['recommendation_type', 'implemented', 'created_at']
    search_fields = ['title', 'farm__name']