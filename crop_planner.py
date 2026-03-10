"""
Comprehensive Crop Planning & Management System
Implements complete workflow: Input → AI Analysis → Actionable Plan → Monitoring
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class CropPlanner:
    def __init__(self):
        self.crop_database = {
            'rice': {
                'duration': 120,
                'water_requirement': 'high',
                'suitable_soil': ['clay', 'loamy', 'clay-loam'],
                'suitable_season': ['kharif'],
                'temp_range': (20, 35),
                'yield_per_ha': '4-6 tons',
                'market_demand': 'high',
                'profit_margin': 'medium',
                'rotation_after': ['wheat', 'pulses', 'vegetables']
            },
            'wheat': {
                'duration': 110,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'clay-loam', 'black'],
                'suitable_season': ['rabi'],
                'temp_range': (10, 25),
                'yield_per_ha': '3-5 tons',
                'market_demand': 'high',
                'profit_margin': 'medium',
                'rotation_after': ['rice', 'cotton', 'sugarcane']
            },
            'cotton': {
                'duration': 150,
                'water_requirement': 'medium',
                'suitable_soil': ['black', 'clay-loam', 'red'],
                'suitable_season': ['kharif'],
                'temp_range': (21, 30),
                'yield_per_ha': '2-3 tons',
                'market_demand': 'high',
                'profit_margin': 'high',
                'rotation_after': ['wheat', 'chickpea', 'mustard']
            },
            'tomato': {
                'duration': 90,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'sandy-loam', 'red'],
                'suitable_season': ['rabi', 'summer'],
                'temp_range': (15, 30),
                'yield_per_ha': '25-40 tons',
                'market_demand': 'very_high',
                'profit_margin': 'high',
                'rotation_after': ['onion', 'cabbage', 'cauliflower']
            },
            'potato': {
                'duration': 100,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'sandy-loam'],
                'suitable_season': ['rabi'],
                'temp_range': (15, 25),
                'yield_per_ha': '20-30 tons',
                'market_demand': 'high',
                'profit_margin': 'medium',
                'rotation_after': ['wheat', 'maize', 'vegetables']
            },
            'corn': {
                'duration': 100,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'clay-loam', 'black'],
                'suitable_season': ['kharif', 'summer'],
                'temp_range': (21, 30),
                'yield_per_ha': '5-8 tons',
                'market_demand': 'high',
                'profit_margin': 'medium',
                'rotation_after': ['wheat', 'potato', 'vegetables']
            },
            'soybean': {
                'duration': 95,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'clay-loam', 'black'],
                'suitable_season': ['kharif'],
                'temp_range': (20, 30),
                'yield_per_ha': '2-3 tons',
                'market_demand': 'high',
                'profit_margin': 'high',
                'rotation_after': ['wheat', 'chickpea', 'mustard']
            },
            'sugarcane': {
                'duration': 365,
                'water_requirement': 'very_high',
                'suitable_soil': ['loamy', 'clay-loam', 'black'],
                'suitable_season': ['kharif'],
                'temp_range': (20, 35),
                'yield_per_ha': '70-100 tons',
                'market_demand': 'high',
                'profit_margin': 'high',
                'rotation_after': ['wheat', 'potato', 'vegetables']
            }
        }
        
        self.resource_costs = {
            'fertilizer_per_ha': 8000,  # INR
            'seeds_per_ha': 3000,
            'irrigation_per_ha': 5000,
            'labor_per_ha': 12000,
            'pesticide_per_ha': 4000
        }
    
    def generate_comprehensive_plan(self, farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main function: Generate complete crop plan
        Input → AI Analysis → Actionable Plan
        """
        # Step 1: Analyze input data
        analysis = self.analyze_farm_conditions(farm_data)
        
        # Step 2: Recommend crops
        crop_recommendations = self.recommend_crops(farm_data, analysis)
        
        # Step 3: Select best crop
        selected_crop = farm_data.get('crop_name') or crop_recommendations[0]['crop']
        
        # Step 4: Generate multi-season plan
        multi_season_plan = self.generate_multi_season_plan(selected_crop, farm_data)
        
        # Step 5: Create crop calendar
        crop_calendar = self.generate_crop_calendar(selected_crop, farm_data)
        
        # Step 6: Predict yield
        yield_prediction = self.predict_yield(selected_crop, farm_data, analysis)
        
        # Step 7: Optimize resources
        resource_plan = self.optimize_resources(selected_crop, farm_data)
        
        # Step 8: Calculate costs & profits
        financial_analysis = self.analyze_costs_profits(selected_crop, farm_data)
        
        # Step 9: Setup alerts & reminders
        alerts_schedule = self.generate_alerts_schedule(crop_calendar)
        
        # Step 10: Stage-specific advice
        stage_advice = self.generate_stage_advice(selected_crop)
        
        return {
            'farm_analysis': analysis,
            'crop_recommendations': crop_recommendations,
            'selected_crop': selected_crop,
            'multi_season_plan': multi_season_plan,
            'crop_calendar': crop_calendar,
            'yield_prediction': yield_prediction,
            'resource_plan': resource_plan,
            'financial_analysis': financial_analysis,
            'alerts_schedule': alerts_schedule,
            'stage_advice': stage_advice,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def analyze_farm_conditions(self, farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze farm conditions and constraints"""
        soil_type = farm_data.get('soil_type', 'loamy')
        soil_ph = float(farm_data.get('soil_ph', 6.5))
        temperature = float(farm_data.get('temperature', 25))
        humidity = float(farm_data.get('humidity', 65))
        rainfall = float(farm_data.get('rainfall', 100))
        
        analysis = {
            'soil_quality': 'good' if 6.0 <= soil_ph <= 7.5 else 'needs_correction',
            'water_availability': 'high' if rainfall > 100 else 'medium' if rainfall > 50 else 'low',
            'climate_suitability': 'optimal' if 20 <= temperature <= 30 else 'moderate',
            'constraints': [],
            'opportunities': []
        }
        
        # Identify constraints
        if soil_ph < 6.0:
            analysis['constraints'].append('Acidic soil - may need lime application')
        elif soil_ph > 7.5:
            analysis['constraints'].append('Alkaline soil - may need sulfur application')
        
        if rainfall < 50:
            analysis['constraints'].append('Low rainfall - irrigation system required')
        
        # Identify opportunities
        if 6.5 <= soil_ph <= 7.0:
            analysis['opportunities'].append('Optimal pH for most crops')
        
        if rainfall > 100:
            analysis['opportunities'].append('Good rainfall - suitable for water-intensive crops')
        
        return analysis
    
    def recommend_crops(self, farm_data: Dict[str, Any], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI-powered crop recommendations"""
        soil_type = farm_data.get('soil_type', 'loamy')
        season = farm_data.get('season', 'kharif')
        temperature = float(farm_data.get('temperature', 25))
        
        recommendations = []
        
        for crop_name, crop_info in self.crop_database.items():
            score = 0
            reasons = []
            
            # Soil suitability
            if soil_type in crop_info['suitable_soil']:
                score += 30
                reasons.append(f"Suitable for {soil_type} soil")
            
            # Season suitability
            if season in crop_info['suitable_season']:
                score += 25
                reasons.append(f"Perfect for {season} season")
            
            # Temperature suitability
            temp_min, temp_max = crop_info['temp_range']
            if temp_min <= temperature <= temp_max:
                score += 25
                reasons.append("Optimal temperature range")
            
            # Market demand
            if crop_info['market_demand'] in ['high', 'very_high']:
                score += 10
                reasons.append("High market demand")
            
            # Profit margin
            if crop_info['profit_margin'] == 'high':
                score += 10
                reasons.append("High profit potential")
            
            if score > 40:  # Only recommend if score > 40
                recommendations.append({
                    'crop': crop_name.title(),
                    'score': min(score, 100),
                    'duration': crop_info['duration'],
                    'yield_per_ha': crop_info['yield_per_ha'],
                    'reasons': reasons,
                    'rotation_options': crop_info['rotation_after']
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:5]  # Top 5 recommendations
    
    def generate_multi_season_plan(self, crop_name: str, farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate 2-3 crop rotation plan for the year"""
        crop_name_lower = crop_name.lower()
        if crop_name_lower not in self.crop_database:
            crop_name_lower = 'rice'
        
        main_crop = self.crop_database[crop_name_lower]
        rotation_crops = main_crop['rotation_after'][:2]
        
        plan = {
            'year_plan': [
                {
                    'sequence': 1,
                    'crop': crop_name.title(),
                    'duration': main_crop['duration'],
                    'season': main_crop['suitable_season'][0],
                    'expected_yield': main_crop['yield_per_ha']
                }
            ],
            'total_crops_per_year': 1
        }
        
        # Add rotation crops if duration allows
        remaining_days = 365 - main_crop['duration']
        if remaining_days > 90 and rotation_crops:
            second_crop_name = rotation_crops[0]
            if second_crop_name in self.crop_database:
                second_crop = self.crop_database[second_crop_name]
                plan['year_plan'].append({
                    'sequence': 2,
                    'crop': second_crop_name.title(),
                    'duration': second_crop['duration'],
                    'season': 'rabi' if main_crop['suitable_season'][0] == 'kharif' else 'kharif',
                    'expected_yield': second_crop['yield_per_ha']
                })
                plan['total_crops_per_year'] = 2
        
        return plan
    
    def generate_crop_calendar(self, crop_name: str, farm_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed crop calendar with key dates"""
        crop_name_lower = crop_name.lower()
        if crop_name_lower not in self.crop_database:
            crop_name_lower = 'rice'
        
        crop_info = self.crop_database[crop_name_lower]
        start_date = datetime.now()
        
        # Define growth stages
        stages = [
            {'name': 'Sowing/Planting', 'duration': 1, 'activities': ['Land preparation', 'Seed sowing', 'Initial irrigation']},
            {'name': 'Seedling', 'duration': int(crop_info['duration'] * 0.15), 'activities': ['Light irrigation', 'Weed control', 'First fertilizer dose']},
            {'name': 'Vegetative', 'duration': int(crop_info['duration'] * 0.35), 'activities': ['Regular irrigation', 'Second fertilizer dose', 'Pest monitoring']},
            {'name': 'Flowering', 'duration': int(crop_info['duration'] * 0.25), 'activities': ['Adequate water supply', 'Third fertilizer dose', 'Disease control']},
            {'name': 'Fruiting/Maturity', 'duration': int(crop_info['duration'] * 0.20), 'activities': ['Reduce irrigation', 'Final pest control', 'Harvest preparation']},
            {'name': 'Harvesting', 'duration': int(crop_info['duration'] * 0.05), 'activities': ['Harvest crop', 'Post-harvest handling', 'Storage preparation']}
        ]
        
        calendar = []
        current_date = start_date
        
        for stage in stages:
            end_date = current_date + timedelta(days=stage['duration'])
            calendar.append({
                'stage': stage['name'],
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'duration_days': stage['duration'],
                'key_activities': stage['activities'],
                'week_number': f"Week {((current_date - start_date).days // 7) + 1}"
            })
            current_date = end_date
        
        return calendar
    
    def predict_yield(self, crop_name: str, farm_data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Predict crop yield based on conditions"""
        crop_name_lower = crop_name.lower()
        if crop_name_lower not in self.crop_database:
            crop_name_lower = 'rice'
        
        crop_info = self.crop_database[crop_name_lower]
        area_ha = float(farm_data.get('area_hectares', 1.0))
        
        # Parse yield range
        yield_range = crop_info['yield_per_ha'].split('-')
        if len(yield_range) == 2:
            min_yield = float(yield_range[0].split()[0])
            max_yield = float(yield_range[1].split()[0])
        else:
            min_yield = max_yield = float(yield_range[0].split()[0])
        
        # Adjust based on conditions
        if analysis['soil_quality'] == 'good':
            predicted_yield_per_ha = (min_yield + max_yield) / 2 * 1.1
        else:
            predicted_yield_per_ha = (min_yield + max_yield) / 2 * 0.9
        
        total_yield = predicted_yield_per_ha * area_ha
        
        return {
            'yield_per_hectare': f"{predicted_yield_per_ha:.1f} tons",
            'total_yield': f"{total_yield:.1f} tons",
            'confidence': 'high' if analysis['soil_quality'] == 'good' else 'medium',
            'factors_affecting': [
                'Soil quality',
                'Weather conditions',
                'Proper fertilization',
                'Pest management'
            ]
        }
    
    def optimize_resources(self, crop_name: str, farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal resource allocation"""
        area_ha = float(farm_data.get('area_hectares', 1.0))
        crop_name_lower = crop_name.lower()
        if crop_name_lower not in self.crop_database:
            crop_name_lower = 'rice'
        
        crop_info = self.crop_database[crop_name_lower]
        
        # Water requirement
        water_req = crop_info['water_requirement']
        if water_req == 'very_high':
            water_mm = 1500
        elif water_req == 'high':
            water_mm = 1200
        else:
            water_mm = 800
        
        return {
            'water': {
                'total_requirement': f"{water_mm * area_ha} mm",
                'per_hectare': f"{water_mm} mm",
                'irrigation_frequency': 'Every 7-10 days' if water_req in ['high', 'very_high'] else 'Every 10-15 days'
            },
            'fertilizer': {
                'nitrogen': f"{120 * area_ha} kg",
                'phosphorus': f"{60 * area_ha} kg",
                'potassium': f"{40 * area_ha} kg",
                'organic_manure': f"{5000 * area_ha} kg"
            },
            'labor': {
                'total_person_days': f"{30 * area_ha} days",
                'peak_requirement': 'During sowing and harvesting'
            },
            'machinery': {
                'tractor_hours': f"{10 * area_ha} hours",
                'harvester_hours': f"{5 * area_ha} hours"
            }
        }
    
    def analyze_costs_profits(self, crop_name: str, farm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate input costs and projected profits"""
        area_ha = float(farm_data.get('area_hectares', 1.0))
        
        # Calculate costs
        total_cost = sum(self.resource_costs.values()) * area_ha
        
        # Estimate revenue (simplified)
        crop_name_lower = crop_name.lower()
        if crop_name_lower not in self.crop_database:
            crop_name_lower = 'rice'
        
        crop_info = self.crop_database[crop_name_lower]
        yield_range = crop_info['yield_per_ha'].split('-')
        avg_yield = float(yield_range[0].split()[0]) * area_ha
        
        # Price per ton (INR) - simplified estimates
        price_per_ton = {
            'rice': 20000, 'wheat': 18000, 'cotton': 50000,
            'tomato': 15000, 'potato': 12000, 'corn': 16000,
            'soybean': 35000, 'sugarcane': 3000
        }
        
        price = price_per_ton.get(crop_name_lower, 20000)
        revenue = avg_yield * price
        profit = revenue - total_cost
        roi = (profit / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            'input_costs': {
                'fertilizer': f"₹{self.resource_costs['fertilizer_per_ha'] * area_ha:,.0f}",
                'seeds': f"₹{self.resource_costs['seeds_per_ha'] * area_ha:,.0f}",
                'irrigation': f"₹{self.resource_costs['irrigation_per_ha'] * area_ha:,.0f}",
                'labor': f"₹{self.resource_costs['labor_per_ha'] * area_ha:,.0f}",
                'pesticide': f"₹{self.resource_costs['pesticide_per_ha'] * area_ha:,.0f}",
                'total': f"₹{total_cost:,.0f}"
            },
            'projected_revenue': f"₹{revenue:,.0f}",
            'projected_profit': f"₹{profit:,.0f}",
            'roi_percentage': f"{roi:.1f}%",
            'break_even_yield': f"{(total_cost / price):.1f} tons",
            'profitability': 'high' if roi > 50 else 'medium' if roi > 25 else 'low'
        }
    
    def generate_alerts_schedule(self, crop_calendar: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate alerts and reminders for critical activities"""
        alerts = []
        
        for stage in crop_calendar:
            for activity in stage['key_activities']:
                alerts.append({
                    'date': stage['start_date'],
                    'stage': stage['stage'],
                    'activity': activity,
                    'priority': 'high' if 'fertilizer' in activity.lower() or 'irrigation' in activity.lower() else 'medium',
                    'reminder_days_before': 2
                })
        
        return alerts
    
    def generate_stage_advice(self, crop_name: str) -> Dict[str, List[str]]:
        """Generate stage-specific advice"""
        return {
            'seedling': [
                'Ensure adequate moisture for germination',
                'Protect from birds and pests',
                'Apply starter fertilizer',
                'Maintain optimal temperature'
            ],
            'vegetative': [
                'Increase irrigation frequency',
                'Apply nitrogen-rich fertilizer',
                'Control weeds regularly',
                'Monitor for pest infestation'
            ],
            'flowering': [
                'Ensure consistent water supply',
                'Apply phosphorus and potassium',
                'Protect from extreme weather',
                'Monitor for diseases'
            ],
            'fruiting': [
                'Reduce nitrogen application',
                'Maintain adequate moisture',
                'Support heavy fruits if needed',
                'Prepare for harvest'
            ],
            'harvesting': [
                'Harvest at right maturity',
                'Handle produce carefully',
                'Dry/cure as required',
                'Store in proper conditions'
            ]
        }

# Global instance
crop_planner = CropPlanner()
