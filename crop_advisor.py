"""
Crop and Fertilizer Recommendation System
"""
import random
from datetime import datetime, timedelta

class CropAdvisor:
    def __init__(self):
        # Crop database with requirements
        self.crop_database = {
            'rice': {
                'name': 'Rice',
                'soil_types': ['clay', 'loamy'],
                'seasons': ['kharif', 'monsoon'],
                'temp_range': (20, 35),
                'rainfall_min': 100,
                'ph_range': (5.5, 7.0),
                'growth_stages': ['seedling', 'tillering', 'flowering', 'maturity'],
                'duration_days': 120,
                'rotation_crops': ['wheat', 'pulses', 'vegetables']
            },
            'wheat': {
                'name': 'Wheat',
                'soil_types': ['loamy', 'clay-loam'],
                'seasons': ['rabi', 'winter'],
                'temp_range': (10, 25),
                'rainfall_min': 50,
                'ph_range': (6.0, 7.5),
                'growth_stages': ['germination', 'tillering', 'jointing', 'heading', 'maturity'],
                'duration_days': 110,
                'rotation_crops': ['rice', 'cotton', 'sugarcane']
            },
            'cotton': {
                'name': 'Cotton',
                'soil_types': ['black', 'loamy', 'sandy-loam'],
                'seasons': ['kharif', 'summer'],
                'temp_range': (21, 35),
                'rainfall_min': 60,
                'ph_range': (6.0, 8.0),
                'growth_stages': ['germination', 'vegetative', 'flowering', 'boll-formation', 'maturity'],
                'duration_days': 150,
                'rotation_crops': ['wheat', 'sorghum', 'pulses']
            },
            'tomato': {
                'name': 'Tomato',
                'soil_types': ['loamy', 'sandy-loam', 'red'],
                'seasons': ['all-season', 'summer', 'winter'],
                'temp_range': (18, 30),
                'rainfall_min': 40,
                'ph_range': (6.0, 7.0),
                'growth_stages': ['seedling', 'vegetative', 'flowering', 'fruiting', 'harvest'],
                'duration_days': 90,
                'rotation_crops': ['beans', 'peas', 'leafy-vegetables']
            },
            'corn': {
                'name': 'Corn/Maize',
                'soil_types': ['loamy', 'sandy-loam', 'clay-loam'],
                'seasons': ['kharif', 'summer'],
                'temp_range': (20, 30),
                'rainfall_min': 60,
                'ph_range': (5.8, 7.0),
                'growth_stages': ['germination', 'vegetative', 'tasseling', 'silking', 'maturity'],
                'duration_days': 100,
                'rotation_crops': ['wheat', 'pulses', 'vegetables']
            },
            'potato': {
                'name': 'Potato',
                'soil_types': ['loamy', 'sandy-loam'],
                'seasons': ['rabi', 'winter'],
                'temp_range': (15, 25),
                'rainfall_min': 50,
                'ph_range': (5.0, 6.5),
                'growth_stages': ['sprouting', 'vegetative', 'tuber-formation', 'bulking', 'maturity'],
                'duration_days': 90,
                'rotation_crops': ['wheat', 'corn', 'legumes']
            },
            'soybean': {
                'name': 'Soybean',
                'soil_types': ['loamy', 'clay-loam', 'black'],
                'seasons': ['kharif', 'monsoon'],
                'temp_range': (20, 30),
                'rainfall_min': 70,
                'ph_range': (6.0, 7.5),
                'growth_stages': ['germination', 'vegetative', 'flowering', 'pod-formation', 'maturity'],
                'duration_days': 100,
                'rotation_crops': ['wheat', 'cotton', 'sorghum']
            },
            'sugarcane': {
                'name': 'Sugarcane',
                'soil_types': ['loamy', 'clay-loam', 'black'],
                'seasons': ['all-season', 'kharif'],
                'temp_range': (20, 35),
                'rainfall_min': 150,
                'ph_range': (6.0, 7.5),
                'growth_stages': ['germination', 'tillering', 'grand-growth', 'maturity'],
                'duration_days': 365,
                'rotation_crops': ['wheat', 'pulses', 'vegetables']
            }
        }
        
        # Fertilizer recommendations by crop and stage
        self.fertilizer_recommendations = {
            'rice': {
                'seedling': {'N': 40, 'P': 20, 'K': 20, 'organic': 'Compost 5 tons/ha', 'chemical': 'Urea 87kg + DAP 110kg + MOP 33kg per ha'},
                'tillering': {'N': 40, 'P': 0, 'K': 20, 'organic': 'Vermicompost 2 tons/ha', 'chemical': 'Urea 87kg + MOP 33kg per ha'},
                'flowering': {'N': 20, 'P': 0, 'K': 20, 'organic': 'Neem cake 200kg/ha', 'chemical': 'Urea 43kg + MOP 33kg per ha'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'wheat': {
                'germination': {'N': 60, 'P': 30, 'K': 20, 'organic': 'FYM 10 tons/ha', 'chemical': 'Urea 130kg + DAP 165kg + MOP 33kg per ha'},
                'tillering': {'N': 40, 'P': 0, 'K': 20, 'organic': 'Vermicompost 2 tons/ha', 'chemical': 'Urea 87kg + MOP 33kg per ha'},
                'jointing': {'N': 20, 'P': 0, 'K': 0, 'organic': 'Liquid biofertilizer', 'chemical': 'Urea 43kg per ha'},
                'heading': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'cotton': {
                'germination': {'N': 40, 'P': 20, 'K': 20, 'organic': 'FYM 8 tons/ha', 'chemical': 'Urea 87kg + DAP 110kg + MOP 33kg per ha'},
                'vegetative': {'N': 60, 'P': 20, 'K': 40, 'organic': 'Compost 3 tons/ha', 'chemical': 'Urea 130kg + DAP 110kg + MOP 67kg per ha'},
                'flowering': {'N': 40, 'P': 0, 'K': 20, 'organic': 'Neem cake 250kg/ha', 'chemical': 'Urea 87kg + MOP 33kg per ha'},
                'boll-formation': {'N': 20, 'P': 0, 'K': 20, 'organic': 'Vermicompost 1 ton/ha', 'chemical': 'Urea 43kg + MOP 33kg per ha'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'tomato': {
                'seedling': {'N': 30, 'P': 40, 'K': 30, 'organic': 'Compost 15 tons/ha', 'chemical': 'Urea 65kg + DAP 220kg + MOP 50kg per ha'},
                'vegetative': {'N': 40, 'P': 20, 'K': 40, 'organic': 'Vermicompost 3 tons/ha', 'chemical': 'Urea 87kg + DAP 110kg + MOP 67kg per ha'},
                'flowering': {'N': 30, 'P': 20, 'K': 40, 'organic': 'Bone meal 200kg/ha', 'chemical': 'Urea 65kg + DAP 110kg + MOP 67kg per ha'},
                'fruiting': {'N': 20, 'P': 10, 'K': 30, 'organic': 'Wood ash 300kg/ha', 'chemical': 'Urea 43kg + DAP 55kg + MOP 50kg per ha'},
                'harvest': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'corn': {
                'germination': {'N': 40, 'P': 30, 'K': 20, 'organic': 'FYM 10 tons/ha', 'chemical': 'Urea 87kg + DAP 165kg + MOP 33kg per ha'},
                'vegetative': {'N': 60, 'P': 20, 'K': 40, 'organic': 'Compost 4 tons/ha', 'chemical': 'Urea 130kg + DAP 110kg + MOP 67kg per ha'},
                'tasseling': {'N': 40, 'P': 0, 'K': 20, 'organic': 'Vermicompost 2 tons/ha', 'chemical': 'Urea 87kg + MOP 33kg per ha'},
                'silking': {'N': 20, 'P': 0, 'K': 0, 'organic': 'Liquid biofertilizer', 'chemical': 'Urea 43kg per ha'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'potato': {
                'sprouting': {'N': 50, 'P': 50, 'K': 50, 'organic': 'FYM 20 tons/ha', 'chemical': 'Urea 109kg + DAP 275kg + MOP 83kg per ha'},
                'vegetative': {'N': 40, 'P': 20, 'K': 40, 'organic': 'Compost 5 tons/ha', 'chemical': 'Urea 87kg + DAP 110kg + MOP 67kg per ha'},
                'tuber-formation': {'N': 30, 'P': 0, 'K': 40, 'organic': 'Wood ash 400kg/ha', 'chemical': 'Urea 65kg + MOP 67kg per ha'},
                'bulking': {'N': 20, 'P': 0, 'K': 20, 'organic': 'Vermicompost 2 tons/ha', 'chemical': 'Urea 43kg + MOP 33kg per ha'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'soybean': {
                'germination': {'N': 20, 'P': 40, 'K': 20, 'organic': 'FYM 5 tons/ha + Rhizobium', 'chemical': 'DAP 220kg + MOP 33kg per ha'},
                'vegetative': {'N': 20, 'P': 20, 'K': 20, 'organic': 'Vermicompost 2 tons/ha', 'chemical': 'Urea 43kg + DAP 110kg + MOP 33kg per ha'},
                'flowering': {'N': 10, 'P': 0, 'K': 20, 'organic': 'Neem cake 150kg/ha', 'chemical': 'Urea 22kg + MOP 33kg per ha'},
                'pod-formation': {'N': 0, 'P': 0, 'K': 20, 'organic': 'Wood ash 200kg/ha', 'chemical': 'MOP 33kg per ha'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            },
            'sugarcane': {
                'germination': {'N': 60, 'P': 40, 'K': 40, 'organic': 'FYM 25 tons/ha', 'chemical': 'Urea 130kg + DAP 220kg + MOP 67kg per ha'},
                'tillering': {'N': 80, 'P': 40, 'K': 60, 'organic': 'Compost 10 tons/ha', 'chemical': 'Urea 174kg + DAP 220kg + MOP 100kg per ha'},
                'grand-growth': {'N': 100, 'P': 20, 'K': 60, 'organic': 'Vermicompost 5 tons/ha', 'chemical': 'Urea 217kg + DAP 110kg + MOP 100kg per ha'},
                'maturity': {'N': 0, 'P': 0, 'K': 0, 'organic': 'No fertilizer', 'chemical': 'No fertilizer'}
            }
        }
        
        # Stage-specific care tips
        self.care_tips = {
            'rice': {
                'seedling': ['Maintain 2-3 cm water level', 'Apply pre-emergence herbicide', 'Monitor for damping off disease'],
                'tillering': ['Increase water level to 5 cm', 'Remove weeds manually', 'Apply first top dressing'],
                'flowering': ['Maintain consistent water supply', 'Monitor for blast disease', 'Apply second top dressing'],
                'maturity': ['Drain field 10 days before harvest', 'Watch for bird damage', 'Check grain moisture']
            },
            'wheat': {
                'germination': ['Light irrigation after sowing', 'Ensure proper seed depth (5 cm)', 'Protect from birds'],
                'tillering': ['First irrigation at 21 days', 'Remove weeds', 'Apply nitrogen fertilizer'],
                'jointing': ['Second irrigation', 'Monitor for aphids', 'Apply fungicide if needed'],
                'heading': ['Critical irrigation stage', 'Protect from lodging', 'Monitor for rust diseases'],
                'maturity': ['Stop irrigation 10 days before harvest', 'Check grain hardness', 'Prepare for harvesting']
            },
            'cotton': {
                'germination': ['Light irrigation', 'Thinning after 15 days', 'Apply pre-emergence herbicide'],
                'vegetative': ['Regular irrigation every 10-12 days', 'Prune lower branches', 'Monitor for sucking pests'],
                'flowering': ['Critical irrigation period', 'Apply growth regulators if needed', 'Monitor for bollworm'],
                'boll-formation': ['Maintain soil moisture', 'Protect from boll shedding', 'Apply potash fertilizer'],
                'maturity': ['Reduce irrigation', 'Monitor boll opening', 'Prepare for picking']
            },
            'tomato': {
                'seedling': ['Transplant at 25-30 days', 'Provide shade for 2-3 days', 'Light irrigation'],
                'vegetative': ['Stake plants at 20 cm height', 'Prune suckers regularly', 'Mulch around plants'],
                'flowering': ['Ensure adequate pollination', 'Maintain consistent moisture', 'Apply calcium spray'],
                'fruiting': ['Support heavy branches', 'Monitor for fruit borer', 'Harvest ripe fruits regularly'],
                'harvest': ['Pick fruits at breaker stage', 'Handle carefully', 'Store in cool place']
            },
            'corn': {
                'germination': ['Ensure proper seed spacing', 'Light irrigation', 'Protect from birds and rodents'],
                'vegetative': ['First irrigation at knee-high stage', 'Earthing up at 30 days', 'Remove weeds'],
                'tasseling': ['Critical water requirement', 'Monitor for stem borer', 'Apply nitrogen fertilizer'],
                'silking': ['Ensure good pollination', 'Maintain soil moisture', 'Protect from fall armyworm'],
                'maturity': ['Check grain moisture', 'Protect from birds', 'Harvest at proper maturity']
            },
            'potato': {
                'sprouting': ['Use certified seed tubers', 'Chitting for 7-10 days', 'Plant at 5-7 cm depth'],
                'vegetative': ['First earthing up at 25 days', 'Regular irrigation', 'Monitor for early blight'],
                'tuber-formation': ['Critical irrigation stage', 'Second earthing up', 'Apply potash fertilizer'],
                'bulking': ['Maintain consistent moisture', 'Monitor for late blight', 'Protect from tuber moth'],
                'maturity': ['Stop irrigation 10 days before harvest', 'Cut foliage if needed', 'Cure tubers after harvest']
            },
            'soybean': {
                'germination': ['Seed treatment with Rhizobium', 'Ensure proper seed rate', 'Light irrigation'],
                'vegetative': ['First irrigation at 30 days', 'Remove weeds', 'Monitor for leaf miners'],
                'flowering': ['Critical water requirement', 'Avoid water stress', 'Monitor for pod borer'],
                'pod-formation': ['Maintain soil moisture', 'Protect from pod shedding', 'Apply foliar spray'],
                'maturity': ['Stop irrigation', 'Check pod maturity', 'Harvest when leaves drop']
            },
            'sugarcane': {
                'germination': ['Plant 2-3 budded setts', 'Light irrigation after planting', 'Gap filling within 30 days'],
                'tillering': ['First earthing up', 'Remove weeds', 'Apply nitrogen fertilizer'],
                'grand-growth': ['Regular irrigation every 10-12 days', 'Second earthing up', 'Monitor for borers'],
                'maturity': ['Stop irrigation 15 days before harvest', 'Check sugar content', 'Harvest at proper maturity']
            }
        }
    
    def recommend_crops(self, soil_type, season, temperature, rainfall, ph):
        """Recommend suitable crops based on conditions"""
        recommendations = []
        
        for crop_key, crop_data in self.crop_database.items():
            score = 0
            reasons = []
            
            # Check soil type
            if soil_type.lower() in crop_data['soil_types']:
                score += 30
                reasons.append(f"Suitable for {soil_type} soil")
            
            # Check season
            if season.lower() in crop_data['seasons'] or 'all-season' in crop_data['seasons']:
                score += 25
                reasons.append(f"Ideal for {season} season")
            
            # Check temperature
            temp_min, temp_max = crop_data['temp_range']
            if temp_min <= temperature <= temp_max:
                score += 25
                reasons.append(f"Temperature within range ({temp_min}-{temp_max}°C)")
            elif abs(temperature - temp_min) <= 5 or abs(temperature - temp_max) <= 5:
                score += 15
                reasons.append(f"Temperature acceptable")
            
            # Check rainfall
            if rainfall >= crop_data['rainfall_min']:
                score += 10
                reasons.append(f"Adequate rainfall")
            
            # Check pH
            ph_min, ph_max = crop_data['ph_range']
            if ph_min <= ph <= ph_max:
                score += 10
                reasons.append(f"pH within range ({ph_min}-{ph_max})")
            
            if score >= 50:  # Threshold for recommendation
                recommendations.append({
                    'crop': crop_data['name'],
                    'crop_key': crop_key,
                    'score': score,
                    'reasons': reasons,
                    'duration': crop_data['duration_days'],
                    'rotation_options': crop_data['rotation_crops']
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:5]  # Top 5 recommendations
    
    def get_fertilizer_recommendation(self, crop, growth_stage, soil_n, soil_p, soil_k, soil_ph, preference='both'):
        """Get fertilizer recommendations for specific crop and stage"""
        crop_key = crop.lower().replace(' ', '').replace('/', '')
        
        if crop_key not in self.fertilizer_recommendations:
            return None
        
        stage_key = growth_stage.lower().replace(' ', '-')
        if stage_key not in self.fertilizer_recommendations[crop_key]:
            # Find closest stage
            stages = list(self.fertilizer_recommendations[crop_key].keys())
            stage_key = stages[0] if stages else None
        
        if not stage_key:
            return None
        
        fert_data = self.fertilizer_recommendations[crop_key][stage_key]
        
        # Calculate adjustments based on soil nutrients
        n_deficit = max(0, fert_data['N'] - soil_n)
        p_deficit = max(0, fert_data['P'] - soil_p)
        k_deficit = max(0, fert_data['K'] - soil_k)
        
        # Determine if nutrients are critical
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
        
        # Generate schedule
        schedule = self._generate_fertilizer_schedule(crop_key, stage_key, preference)
        
        return {
            'crop': crop,
            'stage': growth_stage,
            'npk_required': {'N': fert_data['N'], 'P': fert_data['P'], 'K': fert_data['K']},
            'npk_deficit': {'N': n_deficit, 'P': p_deficit, 'K': k_deficit},
            'organic_recommendation': fert_data['organic'] if preference in ['organic', 'both'] else None,
            'chemical_recommendation': fert_data['chemical'] if preference in ['chemical', 'both'] else None,
            'schedule': schedule,
            'alerts': alerts,
            'care_tips': self.care_tips.get(crop_key, {}).get(stage_key, [])
        }
    
    def _generate_fertilizer_schedule(self, crop_key, stage_key, preference):
        """Generate fertilizer application schedule"""
        schedule = []
        today = datetime.now()
        
        # Week 1
        schedule.append({
            'week': 1,
            'date': today.strftime('%Y-%m-%d'),
            'application': 'Basal dose - Apply before sowing/planting',
            'method': 'Broadcasting and incorporation into soil'
        })
        
        # Week 2
        schedule.append({
            'week': 2,
            'date': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
            'application': 'First top dressing - Apply near plant base',
            'method': 'Side dressing, 5-7 cm away from plant'
        })
        
        return schedule
    
    def get_growth_stage_info(self, crop, current_stage):
        """Get information about current and next growth stages"""
        crop_key = crop.lower().replace(' ', '').replace('/', '')
        
        if crop_key not in self.crop_database:
            return None
        
        stages = self.crop_database[crop_key]['growth_stages']
        current_index = next((i for i, s in enumerate(stages) if s == current_stage.lower().replace(' ', '-')), 0)
        
        next_stage = stages[current_index + 1] if current_index < len(stages) - 1 else None
        
        return {
            'current_stage': stages[current_index],
            'next_stage': next_stage,
            'total_stages': len(stages),
            'progress': int((current_index + 1) / len(stages) * 100)
        }
    
    def generate_comprehensive_plan(self, crop_name, soil_type, soil_n, soil_p, soil_k, soil_ph,
                                    season, temperature, humidity, rainfall, fertilizer_preference='both'):
        """Generate comprehensive crop planning with all details"""
        plan = {
            'input_conditions': {
                'soil_type': soil_type,
                'npk': {'N': soil_n, 'P': soil_p, 'K': soil_k},
                'soil_ph': soil_ph,
                'season': season,
                'temperature': temperature,
                'humidity': humidity,
                'rainfall': rainfall
            }
        }
        
        # If no crop selected, recommend crops
        if not crop_name:
            crop_recommendations = self.recommend_crops(soil_type, season, temperature, rainfall, soil_ph)
            plan['crop_recommendations'] = crop_recommendations
            
            # Use top recommended crop for planning
            if crop_recommendations:
                crop_name = crop_recommendations[0]['crop_key']
                plan['selected_crop'] = crop_recommendations[0]
        else:
            crop_key = crop_name.lower().replace(' ', '').replace('/', '')
            if crop_key in self.crop_database:
                plan['selected_crop'] = {
                    'crop': self.crop_database[crop_key]['name'],
                    'crop_key': crop_key,
                    'duration': self.crop_database[crop_key]['duration_days']
                }
        
        # Generate complete fertilizer plan for all stages
        if crop_name:
            crop_key = crop_name.lower().replace(' ', '').replace('/', '')
            if crop_key in self.crop_database and crop_key in self.fertilizer_recommendations:
                stages = self.crop_database[crop_key]['growth_stages']
                fertilizer_plan = {}
                
                for stage in stages:
                    stage_fert = self.get_fertilizer_recommendation(
                        crop_name, stage, soil_n, soil_p, soil_k, soil_ph, fertilizer_preference
                    )
                    if stage_fert:
                        fertilizer_plan[stage] = stage_fert
                
                plan['fertilizer_plan'] = fertilizer_plan
                
                # Generate complete care timeline
                care_timeline = []
                current_date = datetime.now()
                days_elapsed = 0
                
                for stage in stages:
                    stage_duration = self.crop_database[crop_key]['duration_days'] // len(stages)
                    stage_start = current_date + timedelta(days=days_elapsed)
                    stage_end = stage_start + timedelta(days=stage_duration)
                    
                    care_timeline.append({
                        'stage': stage,
                        'start_date': stage_start.strftime('%Y-%m-%d'),
                        'end_date': stage_end.strftime('%Y-%m-%d'),
                        'duration_days': stage_duration,
                        'care_tips': self.care_tips.get(crop_key, {}).get(stage, []),
                        'fertilizer': fertilizer_plan.get(stage, {})
                    })
                    
                    days_elapsed += stage_duration
                
                plan['care_timeline'] = care_timeline
                plan['total_duration'] = self.crop_database[crop_key]['duration_days']
                plan['expected_harvest'] = (current_date + timedelta(days=plan['total_duration'])).strftime('%Y-%m-%d')
        
        # Soil health alerts
        alerts = []
        if soil_n < 200:
            alerts.append({'type': 'danger', 'message': 'Nitrogen levels are CRITICALLY LOW - immediate application needed'})
        elif soil_n < 300:
            alerts.append({'type': 'warning', 'message': 'Nitrogen levels are below optimal - consider supplementation'})
        
        if soil_p < 10:
            alerts.append({'type': 'danger', 'message': 'Phosphorus levels are CRITICALLY LOW - apply phosphatic fertilizer'})
        elif soil_p < 20:
            alerts.append({'type': 'warning', 'message': 'Phosphorus levels are below optimal'})
        
        if soil_k < 100:
            alerts.append({'type': 'danger', 'message': 'Potassium levels are CRITICALLY LOW - apply potash'})
        elif soil_k < 150:
            alerts.append({'type': 'warning', 'message': 'Potassium levels are below optimal'})
        
        if soil_ph < 5.5:
            alerts.append({'type': 'danger', 'message': 'Soil is HIGHLY ACIDIC - apply lime to increase pH'})
        elif soil_ph < 6.0:
            alerts.append({'type': 'warning', 'message': 'Soil is slightly acidic - monitor pH levels'})
        elif soil_ph > 8.0:
            alerts.append({'type': 'danger', 'message': 'Soil is HIGHLY ALKALINE - apply gypsum to reduce pH'})
        elif soil_ph > 7.5:
            alerts.append({'type': 'warning', 'message': 'Soil is slightly alkaline - monitor pH levels'})
        
        plan['alerts'] = alerts
        
        return plan

# Global instance
crop_advisor = CropAdvisor()
