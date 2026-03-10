from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from datetime import datetime, timedelta

from .models import Farm, Crop, SensorData, DiseaseReport, Recommendation, CropPlan
from .forms import FarmForm, CropForm, DiseaseReportForm
from ml_models.disease_predictor import disease_predictor
from ml_models.research_matcher import research_matcher
from ml_models.crop_advisor import crop_advisor

def home(request):
    """Home page with dashboard"""
    context = {
        'total_farms': Farm.objects.count(),
        'total_reports': DiseaseReport.objects.count(),
        'recent_reports': DiseaseReport.objects.order_by('-reported_at')[:5],
    }
    
    if request.user.is_authenticated:
        user_farms = Farm.objects.filter(farmer=request.user)
        context.update({
            'user_farms': user_farms,
            'user_crops': Crop.objects.filter(farm__farmer=request.user),
        })
    
    return render(request, 'core/home.html', context)

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def farm_list(request):
    """List user's farms"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view your farms.')
        return redirect('login')
    farms = Farm.objects.filter(farmer=request.user)
    return render(request, 'core/farm_list.html', {'farms': farms})

def farm_create(request):
    """Create new farm"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to create a farm.')
        return redirect('login')
        
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = request.user
            farm.save()
            messages.success(request, 'Farm created successfully!')
            return redirect('farm_list')
    else:
        form = FarmForm()
    return render(request, 'core/farm_form.html', {'form': form, 'title': 'Create Farm'})

def disease_dashboard(request):
    """Disease prediction dashboard with crop-specific analysis"""
    # Make accessible without login for demo
    if request.user.is_authenticated:
        farms = Farm.objects.filter(farmer=request.user)
        recent_reports = DiseaseReport.objects.filter(farm__farmer=request.user).order_by('-reported_at')[:10]
    else:
        farms = Farm.objects.all()[:5]  # Show sample farms for demo
        recent_reports = DiseaseReport.objects.all().order_by('-reported_at')[:10]
    
    prediction_result = None
    
    # Handle form submission
    if request.method == 'POST':
        print("=== CROP HEALTH ANALYSIS STARTED ===")
        print("POST data:", request.POST)
        try:
            # Get crop-specific data
            crop_type = request.POST.get('crop_type', 'unknown')
            growth_stage = request.POST.get('growth_stage', 'vegetative')
            
            # Get environmental data
            temperature = float(request.POST.get('temperature', 25))
            humidity = float(request.POST.get('humidity', 65))
            rainfall = float(request.POST.get('rainfall', 2.5))
            soil_ph = float(request.POST.get('soil_ph', 6.5))
            crop_age = int(request.POST.get('crop_age', 45))
            
            # Get optional sensor data
            soil_moisture = request.POST.get('soil_moisture')
            light_intensity = request.POST.get('light_intensity')
            
            print(f"Crop: {crop_type}, Stage: {growth_stage}")
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Rainfall: {rainfall}mm")
            print(f"Soil pH: {soil_ph}, Crop Age: {crop_age} days")
            
            if soil_moisture:
                print(f"Soil Moisture: {soil_moisture}% (IoT Sensor)")
            if light_intensity:
                print(f"Light Intensity: {light_intensity} lux (IoT Sensor)")
            
            # Analyze image if uploaded
            image_analysis = None
            if request.FILES.get('leaf_image'):
                image_file = request.FILES['leaf_image']
                print(f"Image uploaded: {image_file.name}, Size: {image_file.size} bytes")
                image_analysis = disease_predictor.analyze_leaf_image(image_file)
                print(f"Image analysis completed: {image_analysis}")
            
            # Get AI prediction
            print("Running AI/ML disease prediction model...")
            prediction = disease_predictor.predict_disease_risk(
                temperature, humidity, rainfall, soil_ph, crop_age, image_analysis
            )
            
            # Add crop-specific context
            prediction['crop_type'] = crop_type.title()
            prediction['growth_stage'] = growth_stage.title()
            prediction['sensor_data_used'] = bool(soil_moisture or light_intensity)
            
            if soil_moisture:
                prediction['soil_moisture'] = float(soil_moisture)
            if light_intensity:
                prediction['light_intensity'] = float(light_intensity)
            
            prediction_result = prediction
            
            print("=== ANALYSIS COMPLETE ===")
            print(f"Disease: {prediction['disease_name']}, Confidence: {prediction['confidence']}%")
            print(f"Health Score: {prediction['health_score']['score']}")
            print(f"Pests Detected: {len(prediction['pest_detections'])}")
            print(f"Nutrient Deficiencies: {len(prediction['nutrient_deficiencies'])}")
            
            messages.success(request, f'✓ Crop health analysis completed for {crop_type.title()}!')
            
        except Exception as e:
            print(f"ERROR in disease analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error analyzing disease risk: {str(e)}')
    
    context = {
        'farms': farms,
        'recent_reports': recent_reports,
        'prediction_result': prediction_result,
    }
    print("Context prediction_result:", context.get('prediction_result'))
    return render(request, 'core/disease_dashboard.html', context)

def disease_report_create(request):
    """Create disease report"""
    # Check if user is authenticated, if not, redirect to login
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to report diseases.')
        return redirect('login')
        
    if request.method == 'POST':
        form = DiseaseReportForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            report = form.save()
            messages.success(request, 'Disease report submitted successfully!')
            return redirect('disease_dashboard')
    else:
        form = DiseaseReportForm(user=request.user)
    
    return render(request, 'core/disease_report_form.html', {'form': form})

@csrf_exempt
def predict_disease_risk(request):
    """API endpoint for disease risk prediction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract parameters
            temperature = float(data.get('temperature', 25))
            humidity = float(data.get('humidity', 60))
            rainfall = float(data.get('rainfall', 2))
            soil_ph = float(data.get('soil_ph', 6.5))
            crop_age = int(data.get('crop_age_days', 30))
            
            # Get prediction
            prediction = disease_predictor.predict_disease_risk(
                temperature, humidity, rainfall, soil_ph, crop_age
            )
            
            # Get recommendations
            recommendations = disease_predictor.get_recommendations(prediction)
            prediction['recommendations'] = recommendations
            
            return JsonResponse(prediction)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)

def companion_planting(request):
    """Companion planting advisor"""
    recommendations = None
    research_papers = []
    
    if request.method == 'POST':
        primary_crop = request.POST.get('primary_crop')
        garden_size = request.POST.get('garden_size', 'medium')
        
        if primary_crop:
            # Get companion recommendations
            recommendations = research_matcher.find_companion_plants(primary_crop, garden_size)
            
            # Search for related research papers
            research_papers = research_matcher.search_research_papers(
                f"companion planting {primary_crop}", primary_crop
            )
    
    crop_choices = [
        'Tomato', 'Corn', 'Beans', 'Lettuce', 'Carrots', 
        'Peppers', 'Cucumber', 'Squash', 'Basil', 'Marigold'
    ]
    
    context = {
        'crop_choices': crop_choices,
        'recommendations': recommendations,
        'research_papers': research_papers,
    }
    
    return render(request, 'core/companion_planting.html', context)

def disease_map(request):
    """Interactive disease spread map"""
    # Get all disease reports with location data
    reports = DiseaseReport.objects.select_related('farm', 'crop').all()
    
    # Prepare data for map
    map_data = []
    for report in reports:
        map_data.append({
            'lat': report.latitude,
            'lng': report.longitude,
            'disease': report.disease_name,
            'severity': report.severity,
            'farm': report.farm.name,
            'crop': report.crop.get_crop_type_display(),
            'date': report.reported_at.strftime('%Y-%m-%d'),
            'verified': report.verified
        })
    
    context = {
        'map_data': json.dumps(map_data),
        'reports_count': len(map_data)
    }
    
    return render(request, 'core/disease_map.html', context)

def farm_analytics(request, farm_id):
    """Farm analytics dashboard"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view farm analytics.')
        return redirect('login')
        
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user)
    
    # Get recent sensor data
    sensor_data = SensorData.objects.filter(farm=farm).order_by('-timestamp')[:100]
    
    # Get crop health summary
    crops = Crop.objects.filter(farm=farm)
    health_summary = {}
    for crop in crops:
        health_summary[crop.get_crop_type_display()] = crop.health_status
    
    # Get recommendations
    recommendations = Recommendation.objects.filter(farm=farm).order_by('-created_at')[:5]
    
    context = {
        'farm': farm,
        'sensor_data': sensor_data,
        'health_summary': health_summary,
        'recommendations': recommendations,
        'crops': crops
    }
    
    return render(request, 'core/farm_analytics.html', context)

def crop_fertilizer_advisor(request):
    """Crop and Fertilizer Advisor Dashboard"""
    recommendations = None
    
    if request.method == 'POST':
        try:
            # Get form data
            crop_name = request.POST.get('crop_name', '')
            growth_stage = request.POST.get('growth_stage', 'seedling')
            crop_age = int(request.POST.get('crop_age', 30))
            
            soil_type = request.POST.get('soil_type')
            soil_n = float(request.POST.get('soil_n', 250))
            soil_p = float(request.POST.get('soil_p', 15))
            soil_k = float(request.POST.get('soil_k', 150))
            soil_ph = float(request.POST.get('soil_ph', 6.5))
            
            season = request.POST.get('season')
            temperature = float(request.POST.get('temperature', 28))
            humidity = float(request.POST.get('humidity', 65))
            rainfall = float(request.POST.get('rainfall', 100))
            
            fertilizer_preference = request.POST.get('fertilizer_preference', 'both')
            
            recommendations = {}
            
            # Get crop recommendations if no crop selected
            if not crop_name:
                crop_recs = crop_advisor.recommend_crops(
                    soil_type, season, temperature, rainfall, soil_ph
                )
                recommendations['crop_recommendations'] = crop_recs
            
            # Get fertilizer recommendations if crop is selected
            if crop_name:
                fert_rec = crop_advisor.get_fertilizer_recommendation(
                    crop_name, growth_stage, soil_n, soil_p, soil_k, soil_ph, fertilizer_preference
                )
                if fert_rec:
                    recommendations['fertilizer'] = fert_rec
                    recommendations['alerts'] = fert_rec.get('alerts', [])
                    
                    # Get growth stage info
                    stage_info = crop_advisor.get_growth_stage_info(crop_name, growth_stage)
                    if stage_info:
                        recommendations['stage_info'] = stage_info
            else:
                # Check for critical alerts even without crop
                alerts = []
                if soil_n < 200:
                    alerts.append('⚠️ Nitrogen levels are LOW - immediate application needed')
                if soil_p < 10:
                    alerts.append('⚠️ Phosphorus levels are LOW - apply phosphatic fertilizer')
                if soil_k < 100:
                    alerts.append('⚠️ Potassium levels are LOW - apply potash')
                if soil_ph < 5.5:
                    alerts.append('⚠️ Soil is ACIDIC - apply lime to increase pH')
                elif soil_ph > 8.0:
                    alerts.append('⚠️ Soil is ALKALINE - apply gypsum to reduce pH')
                
                if alerts:
                    recommendations['alerts'] = alerts
            
            messages.success(request, 'Recommendations generated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error generating recommendations: {str(e)}')
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    context = {
        'recommendations': recommendations
    }
    
    return render(request, 'core/crop_advisor.html', context)

def crop_planning(request):
    """Comprehensive Crop Planning Dashboard"""
    plan_result = None
    saved_plan = None
    
    if request.method == 'POST':
        try:
            # Get form data
            crop_name = request.POST.get('crop_name', '')
            soil_type = request.POST.get('soil_type')
            soil_n = float(request.POST.get('soil_n', 250))
            soil_p = float(request.POST.get('soil_p', 15))
            soil_k = float(request.POST.get('soil_k', 150))
            soil_ph = float(request.POST.get('soil_ph', 6.5))
            
            season = request.POST.get('season')
            temperature = float(request.POST.get('temperature', 28))
            humidity = float(request.POST.get('humidity', 65))
            rainfall = float(request.POST.get('rainfall', 100))
            
            area_hectares = float(request.POST.get('area_hectares', 1.0))
            fertilizer_preference = request.POST.get('fertilizer_preference', 'both')
            
            # Generate comprehensive plan
            plan_result = crop_advisor.generate_comprehensive_plan(
                crop_name, soil_type, soil_n, soil_p, soil_k, soil_ph,
                season, temperature, humidity, rainfall, fertilizer_preference
            )
            
            # Save plan if user is authenticated
            if request.user.is_authenticated and request.POST.get('save_plan') == 'yes':
                crop_plan = CropPlan.objects.create(
                    user=request.user,
                    crop_name=crop_name if crop_name else plan_result.get('selected_crop', {}).get('crop', 'Unknown'),
                    soil_type=soil_type,
                    soil_nitrogen=soil_n,
                    soil_phosphorus=soil_p,
                    soil_potassium=soil_k,
                    soil_ph=soil_ph,
                    season=season,
                    temperature=temperature,
                    humidity=humidity,
                    rainfall=rainfall,
                    area_hectares=area_hectares,
                    crop_recommendations=plan_result.get('crop_recommendations', []),
                    fertilizer_schedule=plan_result.get('fertilizer_plan', {}),
                    care_instructions=plan_result.get('care_timeline', [])
                )
                saved_plan = crop_plan
                messages.success(request, 'Crop plan saved successfully!')
            
            messages.success(request, 'Crop plan generated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error generating plan: {str(e)}')
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Get user's saved plans
    saved_plans = []
    if request.user.is_authenticated:
        saved_plans = CropPlan.objects.filter(user=request.user, is_active=True)[:10]
    
    context = {
        'plan_result': plan_result,
        'saved_plan': saved_plan,
        'saved_plans': saved_plans
    }
    
    return render(request, 'core/crop_planning.html', context)

def crop_plan_detail(request, plan_id):
    """View detailed crop plan"""
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to view your crop plans.')
        return redirect('login')
    
    plan = get_object_or_404(CropPlan, id=plan_id, user=request.user)
    
    context = {
        'plan': plan
    }
    
    return render(request, 'core/crop_plan_detail.html', context)