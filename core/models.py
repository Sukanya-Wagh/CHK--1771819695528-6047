from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Farm(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    size_acres = models.FloatField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.farmer.username}"

class Crop(models.Model):
    CROP_TYPES = [
        ('corn', 'Corn'),
        ('tomato', 'Tomato'),
        ('wheat', 'Wheat'),
        ('potato', 'Potato'),
        ('soybean', 'Soybean'),
        ('lettuce', 'Lettuce'),
        ('carrot', 'Carrot'),
        ('pepper', 'Pepper'),
    ]
    
    HEALTH_STATUS = [
        ('healthy', 'Healthy'),
        ('at_risk', 'At Risk'),
        ('diseased', 'Diseased'),
        ('recovering', 'Recovering'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    crop_type = models.CharField(max_length=50, choices=CROP_TYPES)
    planting_date = models.DateField()
    expected_harvest = models.DateField()
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS, default='healthy')
    area_acres = models.FloatField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_crop_type_display()} at {self.farm.name}"

class SensorData(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='sensor_data')
    temperature = models.FloatField()  # Celsius
    humidity = models.FloatField()     # Percentage
    soil_moisture = models.FloatField() # Percentage
    ph_level = models.FloatField()
    light_intensity = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Sensor data for {self.farm.name} at {self.timestamp}"

class DiseaseReport(models.Model):
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='disease_reports')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='disease_reports')
    disease_name = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    photo = models.ImageField(upload_to='disease_photos/', null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    affected_area = models.FloatField()  # Square meters
    reported_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.disease_name} at {self.farm.name}"

class ResearchPaper(models.Model):
    title = models.CharField(max_length=500)
    authors = models.TextField()
    abstract = models.TextField()
    publication_date = models.DateField()
    journal = models.CharField(max_length=200)
    doi = models.CharField(max_length=100, unique=True)
    pdf_url = models.URLField(blank=True)
    crops_related = models.ManyToManyField('Crop', blank=True)
    keywords = models.TextField()  # Comma-separated
    citation_count = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title[:100]

class CompanionPlantingRule(models.Model):
    RELATIONSHIP_TYPES = [
        ('beneficial', 'Beneficial'),
        ('neutral', 'Neutral'),
        ('harmful', 'Harmful'),
    ]
    
    primary_crop = models.CharField(max_length=50)
    companion_crop = models.CharField(max_length=50)
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    benefit_description = models.TextField()
    research_paper = models.ForeignKey(ResearchPaper, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_score = models.FloatField()  # 0-1 scale
    
    class Meta:
        unique_together = ['primary_crop', 'companion_crop']
    
    def __str__(self):
        return f"{self.primary_crop} + {self.companion_crop}: {self.relationship_type}"

class Recommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('disease_prevention', 'Disease Prevention'),
        ('companion_planting', 'Companion Planting'),
        ('fertilizer', 'Fertilizer'),
        ('irrigation', 'Irrigation'),
        ('harvest_timing', 'Harvest Timing'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    research_papers = models.ManyToManyField(ResearchPaper, blank=True)
    confidence_score = models.FloatField()
    implemented = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} for {self.farm.name}"

class CropPlan(models.Model):
    """Comprehensive crop planning with all details"""
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crop_plans', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_plans', null=True, blank=True)
    
    # Crop Information
    crop_name = models.CharField(max_length=100)
    crop_variety = models.CharField(max_length=100, blank=True)
    planting_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    area_hectares = models.FloatField(default=1.0)
    
    # Soil Information
    soil_type = models.CharField(max_length=50)
    soil_nitrogen = models.FloatField()  # kg/ha
    soil_phosphorus = models.FloatField()  # kg/ha
    soil_potassium = models.FloatField()  # kg/ha
    soil_ph = models.FloatField()
    
    # Weather/Climate
    season = models.CharField(max_length=50)
    temperature = models.FloatField()  # Celsius
    humidity = models.FloatField()  # Percentage
    rainfall = models.FloatField()  # mm
    
    # Recommendations (stored as JSON)
    crop_recommendations = models.JSONField(default=dict, blank=True)
    fertilizer_schedule = models.JSONField(default=dict, blank=True)
    care_instructions = models.JSONField(default=list, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.crop_name} - {self.created_at.strftime('%Y-%m-%d')}"


class FertilizerRecommendation(models.Model):
    """Fertilizer recommendation based on crop and soil analysis"""
    GROWTH_STAGES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('maturity', 'Maturity'),
    ]

    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='fertilizer_recommendations', null=True, blank=True)
    crop_name = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=50)
    growth_stage = models.CharField(max_length=20, choices=GROWTH_STAGES)

    # Soil nutrient levels
    current_nitrogen = models.FloatField()
    current_phosphorus = models.FloatField()
    current_potassium = models.FloatField()

    # Recommended fertilizer
    fertilizer_type = models.CharField(max_length=100)
    npk_ratio = models.CharField(max_length=20)  # e.g., "20:20:0"
    deficiency_detected = models.CharField(max_length=200)
    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.fertilizer_type}"


class FertilizerQuantity(models.Model):
    """Calculate fertilizer quantity based on farm area"""
    crop_type = models.CharField(max_length=100)
    farm_area = models.FloatField()  # in hectares
    area_unit = models.CharField(max_length=20, default='hectare')
    fertilizer_type = models.CharField(max_length=100)

    # Calculated values
    quantity_per_unit = models.FloatField()  # kg per hectare/acre
    total_quantity = models.FloatField()  # total kg required
    application_method = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fertilizer_type} for {self.crop_type}"


class NutrientDeficiency(models.Model):
    """Detect nutrient deficiency from leaf images or soil data"""
    DEFICIENCY_TYPES = [
        ('nitrogen', 'Nitrogen'),
        ('phosphorus', 'Phosphorus'),
        ('potassium', 'Potassium'),
        ('calcium', 'Calcium'),
        ('magnesium', 'Magnesium'),
        ('iron', 'Iron'),
        ('zinc', 'Zinc'),
    ]

    crop_name = models.CharField(max_length=100)
    deficiency_type = models.CharField(max_length=20, choices=DEFICIENCY_TYPES)
    symptoms = models.TextField()
    leaf_image = models.ImageField(upload_to='leaf_analysis/', null=True, blank=True)

    # Soil data (optional)
    soil_nitrogen = models.FloatField(null=True, blank=True)
    soil_phosphorus = models.FloatField(null=True, blank=True)
    soil_potassium = models.FloatField(null=True, blank=True)

    recommended_fertilizer = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0.0)

    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.deficiency_type} deficiency in {self.crop_name}"


class FertilizerSchedule(models.Model):
    """Fertilizer application schedule for crop lifecycle"""
    crop_name = models.CharField(max_length=100)
    sowing_date = models.DateField()

    # Schedule details (stored as JSON)
    schedule_data = models.JSONField(default=list)
    # Example: [{"day": 0, "stage": "Basal", "fertilizer": "DAP", "quantity": "50kg"}]

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} fertilizer schedule"


class OrganicFertilizer(models.Model):
    """Organic fertilizer suggestions"""
    name = models.CharField(max_length=100)
    nutrient_content = models.JSONField(default=dict)  # {"N": 2.5, "P": 1.5, "K": 1.0}
    suitable_crops = models.TextField()  # Comma-separated
    suitable_soil_types = models.TextField()
    application_rate = models.CharField(max_length=100)
    benefits = models.TextField()

    def __str__(self):
        return self.name


class SoilNutrientAnalysis(models.Model):
    """Soil nutrient analysis and health report"""
    NUTRIENT_LEVELS = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('adequate', 'Adequate'),
        ('high', 'High'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='soil_analyses', null=True, blank=True)

    # Nutrient values
    nitrogen_value = models.FloatField()
    phosphorus_value = models.FloatField()
    potassium_value = models.FloatField()

    # Nutrient levels
    nitrogen_level = models.CharField(max_length=20, choices=NUTRIENT_LEVELS)
    phosphorus_level = models.CharField(max_length=20, choices=NUTRIENT_LEVELS)
    potassium_level = models.CharField(max_length=20, choices=NUTRIENT_LEVELS)

    # Recommendations
    suggested_fertilizers = models.JSONField(default=list)

    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil analysis - {self.analysis_date.strftime('%Y-%m-%d')}"


class WeatherBasedFertilizerAdvice(models.Model):
    """Weather-based fertilizer application advice"""
    location = models.CharField(max_length=200)
    fertilizer_type = models.CharField(max_length=100)

    # Weather data
    weather_condition = models.CharField(max_length=100)
    temperature = models.FloatField()
    rainfall_forecast = models.CharField(max_length=200)
    wind_speed = models.FloatField(null=True, blank=True)

    # Advice
    recommendation = models.TextField()
    best_application_date = models.DateField(null=True, blank=True)
    warning_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather advice for {self.fertilizer_type}"



class FertilizerRecommendation(models.Model):
    """Fertilizer recommendation based on crop and soil analysis"""
    GROWTH_STAGES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('maturity', 'Maturity'),
    ]
    
    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='fertilizer_recommendations', null=True, blank=True)
    crop_name = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=50)
    growth_stage = models.CharField(max_length=20, choices=GROWTH_STAGES)
    
    # Soil nutrient levels
    current_nitrogen = models.FloatField()
    current_phosphorus = models.FloatField()
    current_potassium = models.FloatField()
    
    # Recommended fertilizer
    fertilizer_type = models.CharField(max_length=100)
    npk_ratio = models.CharField(max_length=20)
    deficiency_detected = models.CharField(max_length=200)
    reason = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.crop_name} - {self.fertilizer_type}"


class FertilizerQuantity(models.Model):
    """Calculate fertilizer quantity based on farm area"""
    crop_type = models.CharField(max_length=100)
    farm_area = models.FloatField()
    area_unit = models.CharField(max_length=20, default='hectare')
    fertilizer_type = models.CharField(max_length=100)
    
    quantity_per_unit = models.FloatField()
    total_quantity = models.FloatField()
    application_method = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fertilizer_type} for {self.crop_type}"


class NutrientDeficiency(models.Model):
    """Detect nutrient deficiency from leaf images or soil data"""
    DEFICIENCY_TYPES = [
        ('nitrogen', 'Nitrogen'),
        ('phosphorus', 'Phosphorus'),
        ('potassium', 'Potassium'),
        ('calcium', 'Calcium'),
        ('magnesium', 'Magnesium'),
        ('iron', 'Iron'),
        ('zinc', 'Zinc'),
    ]
    
    crop_name = models.CharField(max_length=100)
    deficiency_type = models.CharField(max_length=20, choices=DEFICIENCY_TYPES)
    symptoms = models.TextField()
    leaf_image = models.ImageField(upload_to='leaf_analysis/', null=True, blank=True)
    
    soil_nitrogen = models.FloatField(null=True, blank=True)
    soil_phosphorus = models.FloatField(null=True, blank=True)
    soil_potassium = models.FloatField(null=True, blank=True)
    
    recommended_fertilizer = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=0.0)
    
    detected_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.deficiency_type} deficiency in {self.crop_name}"


class FertilizerSchedule(models.Model):
    """Fertilizer application schedule for crop lifecycle"""
    crop_name = models.CharField(max_length=100)
    sowing_date = models.DateField()
    schedule_data = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.crop_name} fertilizer schedule"


class OrganicFertilizer(models.Model):
    """Organic fertilizer suggestions"""
    name = models.CharField(max_length=100)
    nutrient_content = models.JSONField(default=dict)
    suitable_crops = models.TextField()
    suitable_soil_types = models.TextField()
    application_rate = models.CharField(max_length=100)
    benefits = models.TextField()
    
    def __str__(self):
        return self.name


class SoilNutrientAnalysis(models.Model):
    """Soil nutrient analysis and health report"""
    NUTRIENT_LEVELS = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('adequate', 'Adequate'),
        ('high', 'High'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='soil_analyses', null=True, blank=True)
    
    nitrogen_value = models.FloatField()
    phosphorus_value = models.FloatField()
    potassium_value = models.FloatField()
    
    nitrogen_level = models.CharField(max_length=20, choices=NUTRIENT_LEVELS)
    phosphorus_level = models.CharField(max_length=20, choices=NUTRIENT_LEVELS)
    potassium_level = models.CharField(max_length=20, choices=NUTRIENT_LEVELS)
    
    suggested_fertilizers = models.JSONField(default=list)
    
    analysis_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Soil analysis - {self.analysis_date.strftime('%Y-%m-%d')}"


class WeatherBasedFertilizerAdvice(models.Model):
    """Weather-based fertilizer application advice"""
    location = models.CharField(max_length=200)
    fertilizer_type = models.CharField(max_length=100)
    
    weather_condition = models.CharField(max_length=100)
    temperature = models.FloatField()
    rainfall_forecast = models.CharField(max_length=200)
    wind_speed = models.FloatField(null=True, blank=True)
    
    recommendation = models.TextField()
    best_application_date = models.DateField(null=True, blank=True)
    warning_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Weather advice for {self.fertilizer_type}"
