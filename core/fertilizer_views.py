from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    FertilizerRecommendation, FertilizerQuantity, NutrientDeficiency,
    FertilizerSchedule, OrganicFertilizer, SoilNutrientAnalysis,
    WeatherBasedFertilizerAdvice, Farm, CropPlan
)
import json
import random


# Crop nutrient requirements database
CROP_NUTRIENT_REQUIREMENTS = {
    'rice': {'N': 120, 'P': 60, 'K': 40, 'growth_stages': ['basal', 'tillering', 'panicle']},
    'wheat': {'N': 150, 'P': 60, 'K': 40, 'growth_stages': ['basal', 'crown_root', 'flowering']},
    'cotton': {'N': 120, 'P': 60, 'K': 60, 'growth_stages': ['vegetative', 'flowering', 'boll']},
    'corn': {'N': 180, 'P': 80, 'K': 60, 'growth_stages': ['seedling', 'vegetative', 'tasseling']},
    'tomato': {'N': 150, 'P': 80, 'K': 120, 'growth_stages': ['vegetative', 'flowering', 'fruiting']},
    'potato': {'N': 150, 'P': 80, 'K': 180, 'growth_stages': ['vegetative', 'tuber_init', 'bulking']},
}


@login_required
def fertilizer_recommendation(request):
    """Feature 1: Fertilizer Recommendation"""
    recommendation = None
    
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name', '').lower()
        soil_type = request.POST.get('soil_type')
        growth_stage = request.POST.get('growth_stage')
        nitrogen = float(request.POST.get('nitrogen', 0))
        phosphorus = float(request.POST.get('phosphorus', 0))
        potassium = float(request.POST.get('potassium', 0))
        
        # Get crop requirements
        crop_req = CROP_NUTRIENT_REQUIREMENTS.get(crop_name, {'N': 100, 'P': 50, 'K': 50})
        
        # Identify deficiencies
        deficiencies = []
        if nitrogen < crop_req['N'] * 0.7:
            deficiencies.append('Nitrogen')
        if phosphorus < crop_req['P'] * 0.7:
            deficiencies.append('Phosphorus')
        if potassium < crop_req['K'] * 0.7:
            deficiencies.append('Potassium')
        
        # Determine fertilizer type and NPK ratio
        if 'Nitrogen' in deficiencies and 'Phosphorus' in deficiencies:
            fertilizer_type = 'DAP (Diammonium Phosphate)'
            npk_ratio = '18:46:0'
        elif 'Nitrogen' in deficiencies:
            fertilizer_type = 'Urea'
            npk_ratio = '46:0:0'
        elif 'Phosphorus' in deficiencies:
            fertilizer_type = 'SSP (Single Super Phosphate)'
            npk_ratio = '0:16:0'
        elif 'Potassium' in deficiencies:
            fertilizer_type = 'MOP (Muriate of Potash)'
            npk_ratio = '0:0:60'
        else:
            fertilizer_type = 'NPK Complex'
            npk_ratio = '20:20:20'
        
        deficiency_text = ', '.join(deficiencies) if deficiencies else 'No major deficiency'
        reason = f"{deficiency_text} detected based on soil test values"
        
        # Save recommendation
        recommendation = FertilizerRecommendation.objects.create(
            crop_name=crop_name.title(),
            soil_type=soil_type,
            growth_stage=growth_stage,
            current_nitrogen=nitrogen,
            current_phosphorus=phosphorus,
            current_potassium=potassium,
            fertilizer_type=fertilizer_type,
            npk_ratio=npk_ratio,
            deficiency_detected=deficiency_text,
            reason=reason
        )
    
    recent_recommendations = FertilizerRecommendation.objects.all().order_by('-created_at')[:10]
    
    context = {
        'recommendation': recommendation,
        'recent_recommendations': recent_recommendations,
        'crop_choices': list(CROP_NUTRIENT_REQUIREMENTS.keys()),
    }
    return render(request, 'core/fertilizer_recommendation.html', context)


@login_required
def fertilizer_quantity_calculator(request):
    """Feature 2: Fertilizer Quantity Calculator"""
    calculation = None
    
    if request.method == 'POST':
        crop_type = request.POST.get('crop_type')
        farm_area = float(request.POST.get('farm_area', 1))
        area_unit = request.POST.get('area_unit', 'hectare')
        fertilizer_type = request.POST.get('fertilizer_type')
        
        # Fertilizer application rates (kg per hectare)
        fertilizer_rates = {
            'Urea': 45,
            'DAP': 50,
            'NPK': 60,
            'MOP': 30,
            'SSP': 40,
        }
        
        quantity_per_unit = fertilizer_rates.get(fertilizer_type, 50)
        
        # Convert to acres if needed
        if area_unit == 'acre':
            quantity_per_unit = quantity_per_unit * 0.4047  # 1 acre = 0.4047 hectares
        
        total_quantity = quantity_per_unit * farm_area
        
        application_methods = {
            'Urea': 'Broadcast application or side dressing. Apply in split doses.',
            'DAP': 'Basal application at sowing time. Mix with soil.',
            'NPK': 'Broadcast and incorporate into soil before planting.',
            'MOP': 'Apply during land preparation or as top dressing.',
            'SSP': 'Basal application. Mix thoroughly with soil.',
        }
        
        calculation = FertilizerQuantity.objects.create(
            crop_type=crop_type,
            farm_area=farm_area,
            area_unit=area_unit,
            fertilizer_type=fertilizer_type,
            quantity_per_unit=quantity_per_unit,
            total_quantity=total_quantity,
            application_method=application_methods.get(fertilizer_type, 'Apply as per standard practices')
        )
    
    recent_calculations = FertilizerQuantity.objects.all().order_by('-created_at')[:10]
    
    context = {
        'calculation': calculation,
        'recent_calculations': recent_calculations,
    }
    return render(request, 'core/fertilizer_quantity.html', context)


@login_required
def nutrient_deficiency_detection(request):
    """Feature 3: Nutrient Deficiency Detection"""
    deficiency = None
    
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        detection_method = request.POST.get('detection_method')
        
        if detection_method == 'soil_data':
            nitrogen = float(request.POST.get('nitrogen', 0))
            phosphorus = float(request.POST.get('phosphorus', 0))
            potassium = float(request.POST.get('potassium', 0))
            
            # Analyze deficiency
            deficiencies = []
            symptoms = []
            
            if nitrogen < 40:
                deficiencies.append('nitrogen')
                symptoms.append('Yellowing of older leaves, stunted growth')
            if phosphorus < 20:
                deficiencies.append('phosphorus')
                symptoms.append('Purple or dark green leaves, poor root development')
            if potassium < 30:
                deficiencies.append('potassium')
                symptoms.append('Brown leaf edges, weak stems')
            
            if deficiencies:
                primary_deficiency = deficiencies[0]
                symptom_text = '; '.join(symptoms)
            else:
                primary_deficiency = 'nitrogen'
                symptom_text = 'No major deficiency detected'
            
            fertilizer_map = {
                'nitrogen': 'Urea (46-0-0)',
                'phosphorus': 'DAP (18-46-0)',
                'potassium': 'MOP (0-0-60)',
            }
            
            deficiency = NutrientDeficiency.objects.create(
                crop_name=crop_name,
                deficiency_type=primary_deficiency,
                symptoms=symptom_text,
                soil_nitrogen=nitrogen,
                soil_phosphorus=phosphorus,
                soil_potassium=potassium,
                recommended_fertilizer=fertilizer_map.get(primary_deficiency, 'NPK Complex'),
                confidence_score=0.85
            )
        
        elif detection_method == 'leaf_image':
            # Simulated AI analysis
            deficiency = NutrientDeficiency.objects.create(
                crop_name=crop_name,
                deficiency_type='nitrogen',
                symptoms='Yellow leaves, pale green color',
                recommended_fertilizer='Urea (46-0-0)',
                confidence_score=0.78
            )
    
    recent_detections = NutrientDeficiency.objects.all().order_by('-detected_at')[:10]
    
    context = {
        'deficiency': deficiency,
        'recent_detections': recent_detections,
    }
    return render(request, 'core/nutrient_deficiency.html', context)


@login_required
def fertilizer_schedule(request):
    """Feature 4: Fertilizer Schedule"""
    schedule = None
    
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name', '').lower()
        sowing_date_str = request.POST.get('sowing_date')
        sowing_date = datetime.strptime(sowing_date_str, '%Y-%m-%d').date()
        
        # Crop-specific schedules
        schedules = {
            'rice': [
                {'day': 0, 'stage': 'Basal Dose', 'fertilizer': 'DAP', 'quantity': '50 kg/ha', 'npk': '18:46:0'},
                {'day': 25, 'stage': 'Tillering', 'fertilizer': 'Urea', 'quantity': '45 kg/ha', 'npk': '46:0:0'},
                {'day': 45, 'stage': 'Panicle Initiation', 'fertilizer': 'MOP', 'quantity': '30 kg/ha', 'npk': '0:0:60'},
            ],
            'wheat': [
                {'day': 0, 'stage': 'Basal Dose', 'fertilizer': 'DAP', 'quantity': '60 kg/ha', 'npk': '18:46:0'},
                {'day': 21, 'stage': 'Crown Root', 'fertilizer': 'Urea', 'quantity': '50 kg/ha', 'npk': '46:0:0'},
                {'day': 60, 'stage': 'Flowering', 'fertilizer': 'Urea', 'quantity': '40 kg/ha', 'npk': '46:0:0'},
            ],
            'cotton': [
                {'day': 0, 'stage': 'Basal Dose', 'fertilizer': 'NPK', 'quantity': '60 kg/ha', 'npk': '20:20:0'},
                {'day': 30, 'stage': 'Vegetative', 'fertilizer': 'Urea', 'quantity': '45 kg/ha', 'npk': '46:0:0'},
                {'day': 60, 'stage': 'Flowering', 'fertilizer': 'MOP', 'quantity': '40 kg/ha', 'npk': '0:0:60'},
            ],
            'corn': [
                {'day': 0, 'stage': 'Basal Dose', 'fertilizer': 'DAP', 'quantity': '70 kg/ha', 'npk': '18:46:0'},
                {'day': 30, 'stage': 'Vegetative', 'fertilizer': 'Urea', 'quantity': '60 kg/ha', 'npk': '46:0:0'},
                {'day': 50, 'stage': 'Tasseling', 'fertilizer': 'MOP', 'quantity': '35 kg/ha', 'npk': '0:0:60'},
            ],
        }
        
        schedule_data = schedules.get(crop_name, schedules['rice'])
        
        # Add actual dates
        for item in schedule_data:
            item['date'] = (sowing_date + timedelta(days=item['day'])).strftime('%Y-%m-%d')
        
        schedule = FertilizerSchedule.objects.create(
            crop_name=crop_name.title(),
            sowing_date=sowing_date,
            schedule_data=schedule_data
        )
    
    recent_schedules = FertilizerSchedule.objects.all().order_by('-created_at')[:10]
    
    context = {
        'schedule': schedule,
        'recent_schedules': recent_schedules,
    }
    return render(request, 'core/fertilizer_schedule.html', context)


@login_required
def organic_fertilizer_suggestion(request):
    """Feature 5: Organic Fertilizer Suggestion"""
    suggestions = []
    
    if request.method == 'POST':
        crop_type = request.POST.get('crop_type', '').lower()
        soil_condition = request.POST.get('soil_condition', '').lower()
        
        # Get or create organic fertilizers
        organic_options = [
            {
                'name': 'Vermicompost',
                'nutrient_content': {'N': 2.0, 'P': 1.5, 'K': 1.5},
                'suitable_crops': 'All crops, especially vegetables',
                'suitable_soil_types': 'All soil types',
                'application_rate': '2-3 tons per hectare',
                'benefits': 'Improves soil structure, water retention, and microbial activity'
            },
            {
                'name': 'Neem Cake',
                'nutrient_content': {'N': 5.0, 'P': 1.0, 'K': 1.4},
                'suitable_crops': 'Cotton, vegetables, fruits',
                'suitable_soil_types': 'All soil types',
                'application_rate': '200-250 kg per hectare',
                'benefits': 'Natural pesticide, improves nitrogen availability'
            },
            {
                'name': 'Cow Dung Manure',
                'nutrient_content': {'N': 0.5, 'P': 0.3, 'K': 0.5},
                'suitable_crops': 'All crops',
                'suitable_soil_types': 'Sandy and loamy soils',
                'application_rate': '10-15 tons per hectare',
                'benefits': 'Enhances soil fertility and organic matter content'
            },
            {
                'name': 'Compost',
                'nutrient_content': {'N': 1.5, 'P': 1.0, 'K': 1.5},
                'suitable_crops': 'All crops',
                'suitable_soil_types': 'All soil types',
                'application_rate': '5-10 tons per hectare',
                'benefits': 'Improves soil health, water retention, and nutrient availability'
            },
        ]
        
        for option in organic_options:
            obj, created = OrganicFertilizer.objects.get_or_create(
                name=option['name'],
                defaults=option
            )
            suggestions.append(obj)
    
    all_organic = OrganicFertilizer.objects.all()
    
    context = {
        'suggestions': suggestions,
        'all_organic': all_organic,
    }
    return render(request, 'core/organic_fertilizer.html', context)


@login_required
def soil_nutrient_analysis(request):
    """Feature 6: Soil Nutrient Analysis"""
    analysis = None
    
    if request.method == 'POST':
        nitrogen = float(request.POST.get('nitrogen', 0))
        phosphorus = float(request.POST.get('phosphorus', 0))
        potassium = float(request.POST.get('potassium', 0))
        
        # Determine nutrient levels
        def get_level(value, thresholds):
            if value < thresholds[0]:
                return 'low'
            elif value < thresholds[1]:
                return 'moderate'
            elif value < thresholds[2]:
                return 'adequate'
            else:
                return 'high'
        
        n_level = get_level(nitrogen, [40, 80, 120])
        p_level = get_level(phosphorus, [20, 40, 60])
        k_level = get_level(potassium, [30, 60, 90])
        
        # Generate fertilizer recommendations
        fertilizers = []
        if n_level == 'low':
            fertilizers.append({'name': 'Urea', 'quantity': '50 kg/ha', 'reason': 'Low nitrogen'})
        if p_level == 'low':
            fertilizers.append({'name': 'DAP', 'quantity': '40 kg/ha', 'reason': 'Low phosphorus'})
        if k_level == 'low':
            fertilizers.append({'name': 'MOP', 'quantity': '30 kg/ha', 'reason': 'Low potassium'})
        
        if not fertilizers:
            fertilizers.append({'name': 'Maintenance dose', 'quantity': 'NPK 20:20:20', 'reason': 'Balanced nutrition'})
        
        analysis = SoilNutrientAnalysis.objects.create(
            nitrogen_value=nitrogen,
            phosphorus_value=phosphorus,
            potassium_value=potassium,
            nitrogen_level=n_level,
            phosphorus_level=p_level,
            potassium_level=k_level,
            suggested_fertilizers=fertilizers
        )
    
    recent_analyses = SoilNutrientAnalysis.objects.all().order_by('-analysis_date')[:10]
    
    context = {
        'analysis': analysis,
        'recent_analyses': recent_analyses,
    }
    return render(request, 'core/soil_analysis.html', context)


@login_required
def weather_fertilizer_advice(request):
    """Feature 7: Weather Based Fertilizer Advice"""
    advice = None
    
    if request.method == 'POST':
        location = request.POST.get('location')
        fertilizer_type = request.POST.get('fertilizer_type')
        
        # Simulated weather data (in production, use weather API)
        import random
        weather_conditions = ['Clear', 'Cloudy', 'Light Rain', 'Heavy Rain', 'Windy']
        weather = random.choice(weather_conditions)
        temp = random.uniform(20, 35)
        
        # Generate advice based on weather
        if 'Rain' in weather:
            recommendation = f"Heavy rain expected. Postpone fertilizer application by 2-3 days to avoid nutrient leaching."
            warning = "⚠️ Weather Alert: Rain forecast detected"
            best_date = (datetime.now() + timedelta(days=3)).date()
        elif weather == 'Windy':
            recommendation = "High wind conditions. Avoid foliar spray. Soil application recommended."
            warning = "⚠️ Wind Alert: Not suitable for spray application"
            best_date = (datetime.now() + timedelta(days=1)).date()
        elif temp > 32:
            recommendation = "High temperature. Apply fertilizer in early morning or evening to reduce volatilization."
            warning = "⚠️ Temperature Alert: Apply during cooler hours"
            best_date = datetime.now().date()
        else:
            recommendation = "Weather conditions are favorable for fertilizer application."
            warning = ""
            best_date = datetime.now().date()
        
        advice = WeatherBasedFertilizerAdvice.objects.create(
            location=location,
            fertilizer_type=fertilizer_type,
            weather_condition=weather,
            temperature=temp,
            rainfall_forecast=f"{weather} conditions",
            recommendation=recommendation,
            best_application_date=best_date,
            warning_message=warning
        )
    
    recent_advice = WeatherBasedFertilizerAdvice.objects.all().order_by('-created_at')[:10]
    
    context = {
        'advice': advice,
        'recent_advice': recent_advice,
    }
    return render(request, 'core/weather_fertilizer.html', context)


@login_required
def fertilizer_dashboard(request):
    """Main dashboard for all fertilizer features"""
    context = {
        'total_recommendations': FertilizerRecommendation.objects.count(),
        'total_analyses': SoilNutrientAnalysis.objects.count(),
        'total_schedules': FertilizerSchedule.objects.count(),
        'recent_recommendations': FertilizerRecommendation.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'core/fertilizer_dashboard.html', context)
