"""
KrushiRakshak AI - Smart Fertilizer Management System
Advanced AI-powered fertilizer recommendation with cost analysis and scheduling
"""

import json
from datetime import datetime, timedelta


class SmartFertilizerAI:
    """Advanced AI system for comprehensive fertilizer management"""
    
    def __init__(self):
        self.crop_requirements = self._load_crop_requirements()
        self.fertilizer_prices = self._load_fertilizer_prices()
        self.growth_stages = self._load_growth_stages()
    
    def _load_crop_requirements(self):
        """Crop-specific nutrient requirements (kg/ha)"""
        return {
            'rice': {'N': 120, 'P': 60, 'K': 40, 'optimal_ph': [5.5, 6.5]},
            'wheat': {'N': 150, 'P': 60, 'K': 40, 'optimal_ph': [6.0, 7.5]},
            'cotton': {'N': 120, 'P': 60, 'K': 60, 'optimal_ph': [6.0, 7.5]},
            'corn': {'N': 180, 'P': 80, 'K': 60, 'optimal_ph': [5.8, 7.0]},
            'tomato': {'N': 150, 'P': 80, 'K': 120, 'optimal_ph': [6.0, 7.0]},
            'potato': {'N': 150, 'P': 80, 'K': 180, 'optimal_ph': [5.0, 6.5]},
            'sugarcane': {'N': 200, 'P': 100, 'K': 100, 'optimal_ph': [6.0, 7.5]},
            'soybean': {'N': 40, 'P': 80, 'K': 40, 'optimal_ph': [6.0, 7.0]},
        }
    
    def _load_fertilizer_prices(self):
        """Current market prices (INR per kg)"""
        return {
            'Urea': 6.5,
            'DAP': 27.0,
            'MOP': 17.0,
            'NPK 20:20:20': 25.0,
            'NPK 10:26:26': 24.0,
            'SSP': 8.0,
            'Vermicompost': 5.0,
            'Neem Cake': 20.0,
            'FYM': 2.0,
        }
    
    def _load_growth_stages(self):
        """Crop growth stages and fertilizer timing"""
        return {
            'rice': [
                {'stage': 'Basal', 'days': 0, 'N': 40, 'P': 100, 'K': 50},
                {'stage': 'Tillering', 'days': 25, 'N': 40, 'P': 0, 'K': 0},
                {'stage': 'Panicle Initiation', 'days': 45, 'N': 20, 'P': 0, 'K': 50},
            ],
            'wheat': [
                {'stage': 'Basal', 'days': 0, 'N': 50, 'P': 100, 'K': 50},
                {'stage': 'Crown Root', 'days': 21, 'N': 30, 'P': 0, 'K': 0},
                {'stage': 'Flowering', 'days': 60, 'N': 20, 'P': 0, 'K': 50},
            ],
            'cotton': [
                {'stage': 'Basal', 'days': 0, 'N': 40, 'P': 100, 'K': 40},
                {'stage': 'Vegetative', 'days': 30, 'N': 40, 'P': 0, 'K': 20},
                {'stage': 'Flowering', 'days': 60, 'N': 20, 'P': 0, 'K': 40},
            ],
            'tomato': [
                {'stage': 'Transplanting', 'days': 0, 'N': 40, 'P': 100, 'K': 40},
                {'stage': 'Vegetative', 'days': 21, 'N': 40, 'P': 0, 'K': 40},
                {'stage': 'Flowering', 'days': 42, 'N': 30, 'P': 0, 'K': 40},
                {'stage': 'Fruiting', 'days': 63, 'N': 20, 'P': 0, 'K': 40},
            ],
        }
    
    def analyze_and_recommend(self, crop_type, farm_area, area_unit, soil_type, season,
                              nitrogen, phosphorus, potassium, ph, weather_condition='normal'):
        """
        Complete AI analysis and recommendation
        Returns comprehensive fertilizer plan with cost and schedule
        """
        
        # Convert area to hectares
        area_ha = farm_area if area_unit == 'hectare' else farm_area * 0.4047
        
        # Get crop requirements
        crop_req = self.crop_requirements.get(crop_type.lower(), 
                                              {'N': 100, 'P': 50, 'K': 50, 'optimal_ph': [6.0, 7.0]})
        
        # 1. Detect Deficiencies
        deficiencies = self._detect_deficiencies(nitrogen, phosphorus, potassium, ph, crop_req)
        
        # 2. Calculate Required Nutrients
        required_nutrients = self._calculate_required_nutrients(
            nitrogen, phosphorus, potassium, crop_req, area_ha
        )
        
        # 3. Recommend Fertilizers
        chemical_fertilizers = self._recommend_chemical_fertilizers(required_nutrients, area_ha)
        organic_alternatives = self._recommend_organic_fertilizers(crop_type, soil_type, area_ha)
        
        # 4. Generate Application Schedule
        schedule = self._generate_schedule(crop_type, chemical_fertilizers, season)
        
        # 5. Calculate Costs
        cost_analysis = self._calculate_costs(chemical_fertilizers, organic_alternatives)
        
        # 6. Predict Yield Improvement
        yield_prediction = self._predict_yield_improvement(deficiencies, crop_type)
        
        # 7. Sustainability Score
        sustainability = self._calculate_sustainability_score(chemical_fertilizers, organic_alternatives)
        
        # 8. Weather-based Adjustments
        weather_advice = self._get_weather_advice(weather_condition, schedule)
        
        return {
            'deficiencies': deficiencies,
            'required_nutrients': required_nutrients,
            'chemical_fertilizers': chemical_fertilizers,
            'organic_alternatives': organic_alternatives,
            'schedule': schedule,
            'cost_analysis': cost_analysis,
            'yield_prediction': yield_prediction,
            'sustainability_score': sustainability,
            'weather_advice': weather_advice,
            'summary': self._generate_summary(crop_type, area_ha, deficiencies, cost_analysis)
        }
    
    def _detect_deficiencies(self, n, p, k, ph, crop_req):
        """Detect nutrient deficiencies"""
        deficiencies = []
        
        if n < crop_req['N'] * 0.6:
            deficiencies.append({
                'nutrient': 'Nitrogen (N)',
                'current': n,
                'required': crop_req['N'],
                'severity': 'High' if n < crop_req['N'] * 0.4 else 'Medium',
                'symptoms': 'Yellowing of older leaves, stunted growth'
            })
        
        if p < crop_req['P'] * 0.6:
            deficiencies.append({
                'nutrient': 'Phosphorus (P)',
                'current': p,
                'required': crop_req['P'],
                'severity': 'High' if p < crop_req['P'] * 0.4 else 'Medium',
                'symptoms': 'Purple/dark green leaves, poor root development'
            })
        
        if k < crop_req['K'] * 0.6:
            deficiencies.append({
                'nutrient': 'Potassium (K)',
                'current': k,
                'required': crop_req['K'],
                'severity': 'High' if k < crop_req['K'] * 0.4 else 'Medium',
                'symptoms': 'Brown leaf edges, weak stems'
            })
        
        # pH check
        optimal_ph = crop_req['optimal_ph']
        if ph < optimal_ph[0] or ph > optimal_ph[1]:
            deficiencies.append({
                'nutrient': 'pH Level',
                'current': ph,
                'required': f"{optimal_ph[0]}-{optimal_ph[1]}",
                'severity': 'Medium',
                'symptoms': 'Nutrient lockout, poor nutrient availability'
            })
        
        return deficiencies
    
    def _calculate_required_nutrients(self, current_n, current_p, current_k, crop_req, area_ha):
        """Calculate exact nutrient requirements"""
        return {
            'nitrogen': max(0, (crop_req['N'] - current_n) * area_ha),
            'phosphorus': max(0, (crop_req['P'] - current_p) * area_ha),
            'potassium': max(0, (crop_req['K'] - current_k) * area_ha),
        }
    
    def _recommend_chemical_fertilizers(self, required, area_ha):
        """Recommend chemical fertilizers with quantities"""
        fertilizers = []
        
        n_needed = required['nitrogen']
        p_needed = required['phosphorus']
        k_needed = required['potassium']
        
        # DAP for Phosphorus (18-46-0)
        if p_needed > 0:
            dap_qty = (p_needed / 0.46) * 1.1  # 46% P2O5, 10% buffer
            fertilizers.append({
                'name': 'DAP (Diammonium Phosphate)',
                'npk': '18-46-0',
                'quantity_kg': round(dap_qty, 2),
                'quantity_per_ha': round(dap_qty / area_ha, 2),
                'application': 'Basal application at sowing',
                'nutrients_provided': {
                    'N': round(dap_qty * 0.18, 2),
                    'P': round(dap_qty * 0.46, 2),
                    'K': 0
                }
            })
            n_needed -= dap_qty * 0.18  # DAP also provides nitrogen
        
        # Urea for Nitrogen (46-0-0)
        if n_needed > 0:
            urea_qty = (n_needed / 0.46) * 1.1
            fertilizers.append({
                'name': 'Urea',
                'npk': '46-0-0',
                'quantity_kg': round(urea_qty, 2),
                'quantity_per_ha': round(urea_qty / area_ha, 2),
                'application': 'Split application - 2-3 doses',
                'nutrients_provided': {
                    'N': round(urea_qty * 0.46, 2),
                    'P': 0,
                    'K': 0
                }
            })
        
        # MOP for Potassium (0-0-60)
        if k_needed > 0:
            mop_qty = (k_needed / 0.60) * 1.1
            fertilizers.append({
                'name': 'MOP (Muriate of Potash)',
                'npk': '0-0-60',
                'quantity_kg': round(mop_qty, 2),
                'quantity_per_ha': round(mop_qty / area_ha, 2),
                'application': 'Split application with top dressing',
                'nutrients_provided': {
                    'N': 0,
                    'P': 0,
                    'K': round(mop_qty * 0.60, 2)
                }
            })
        
        return fertilizers
    
    def _recommend_organic_fertilizers(self, crop_type, soil_type, area_ha):
        """Recommend organic alternatives"""
        return [
            {
                'name': 'Vermicompost',
                'quantity_kg': round(2000 * area_ha, 2),
                'quantity_per_ha': 2000,
                'benefits': 'Improves soil structure, water retention, microbial activity',
                'application': 'Apply 2-3 weeks before sowing, mix with soil',
                'npk_content': '2-1.5-1.5'
            },
            {
                'name': 'Neem Cake',
                'quantity_kg': round(200 * area_ha, 2),
                'quantity_per_ha': 200,
                'benefits': 'Natural pesticide, improves nitrogen availability',
                'application': 'Mix with soil during land preparation',
                'npk_content': '5-1-1.4'
            },
            {
                'name': 'FYM (Farm Yard Manure)',
                'quantity_kg': round(10000 * area_ha, 2),
                'quantity_per_ha': 10000,
                'benefits': 'Enhances soil fertility and organic matter',
                'application': 'Apply well-decomposed FYM before sowing',
                'npk_content': '0.5-0.3-0.5'
            },
        ]
    
    def _generate_schedule(self, crop_type, fertilizers, season):
        """Generate week-wise fertilizer application schedule"""
        stages = self.growth_stages.get(crop_type.lower(), self.growth_stages['rice'])
        
        schedule = []
        sowing_date = datetime.now()
        
        for stage_info in stages:
            application_date = sowing_date + timedelta(days=stage_info['days'])
            week_number = stage_info['days'] // 7
            
            # Determine which fertilizers to apply
            fertilizers_to_apply = []
            
            if stage_info['N'] > 0:
                urea_fert = next((f for f in fertilizers if 'Urea' in f['name']), None)
                if urea_fert:
                    qty = (stage_info['N'] / 100) * urea_fert['quantity_kg']
                    fertilizers_to_apply.append({
                        'fertilizer': 'Urea',
                        'quantity': round(qty, 2)
                    })
            
            if stage_info['P'] > 0:
                dap_fert = next((f for f in fertilizers if 'DAP' in f['name']), None)
                if dap_fert:
                    qty = (stage_info['P'] / 100) * dap_fert['quantity_kg']
                    fertilizers_to_apply.append({
                        'fertilizer': 'DAP',
                        'quantity': round(qty, 2)
                    })
            
            if stage_info['K'] > 0:
                mop_fert = next((f for f in fertilizers if 'MOP' in f['name']), None)
                if mop_fert:
                    qty = (stage_info['K'] / 100) * mop_fert['quantity_kg']
                    fertilizers_to_apply.append({
                        'fertilizer': 'MOP',
                        'quantity': round(qty, 2)
                    })
            
            schedule.append({
                'week': week_number,
                'day': stage_info['days'],
                'date': application_date.strftime('%Y-%m-%d'),
                'stage': stage_info['stage'],
                'fertilizers': fertilizers_to_apply,
                'instructions': self._get_application_instructions(stage_info['stage'])
            })
        
        return schedule
    
    def _get_application_instructions(self, stage):
        """Get stage-specific application instructions"""
        instructions = {
            'Basal': 'Mix fertilizer with soil during final land preparation. Ensure uniform distribution.',
            'Tillering': 'Apply as top dressing. Irrigate immediately after application.',
            'Vegetative': 'Broadcast uniformly. Apply during cool hours (morning/evening).',
            'Flowering': 'Apply near root zone. Avoid contact with leaves.',
            'Fruiting': 'Foliar spray or soil application. Maintain adequate moisture.',
            'Panicle Initiation': 'Apply with irrigation water. Ensure proper drainage.',
        }
        return instructions.get(stage, 'Apply as per standard practices.')
    
    def _calculate_costs(self, chemical_fertilizers, organic_alternatives):
        """Calculate total cost with breakdown"""
        chemical_cost = sum(
            f['quantity_kg'] * self.fertilizer_prices.get(f['name'].split()[0], 10)
            for f in chemical_fertilizers
        )
        
        organic_cost = sum(
            o['quantity_kg'] * self.fertilizer_prices.get(o['name'], 5)
            for o in organic_alternatives
        )
        
        return {
            'chemical_total': round(chemical_cost, 2),
            'organic_total': round(organic_cost, 2),
            'chemical_breakdown': [
                {
                    'fertilizer': f['name'],
                    'quantity': f['quantity_kg'],
                    'rate': self.fertilizer_prices.get(f['name'].split()[0], 10),
                    'cost': round(f['quantity_kg'] * self.fertilizer_prices.get(f['name'].split()[0], 10), 2)
                }
                for f in chemical_fertilizers
            ],
            'organic_breakdown': [
                {
                    'fertilizer': o['name'],
                    'quantity': o['quantity_kg'],
                    'rate': self.fertilizer_prices.get(o['name'], 5),
                    'cost': round(o['quantity_kg'] * self.fertilizer_prices.get(o['name'], 5), 2)
                }
                for o in organic_alternatives
            ],
            'savings_with_organic': round(chemical_cost - organic_cost, 2) if organic_cost < chemical_cost else 0
        }
    
    def _predict_yield_improvement(self, deficiencies, crop_type):
        """Predict expected yield improvement"""
        if not deficiencies:
            return {
                'improvement_percentage': '5-10%',
                'description': 'Maintenance fertilization will sustain current yield levels',
                'confidence': 'Medium'
            }
        
        severity_count = sum(1 for d in deficiencies if d.get('severity') == 'High')
        
        if severity_count >= 2:
            return {
                'improvement_percentage': '25-40%',
                'description': 'Significant yield improvement expected with proper fertilization',
                'confidence': 'High'
            }
        elif severity_count == 1:
            return {
                'improvement_percentage': '15-25%',
                'description': 'Moderate yield improvement expected',
                'confidence': 'High'
            }
        else:
            return {
                'improvement_percentage': '10-15%',
                'description': 'Good yield improvement expected',
                'confidence': 'Medium'
            }
    
    def _calculate_sustainability_score(self, chemical, organic):
        """Calculate sustainability score (0-10)"""
        # Higher score for more organic usage
        total_chemical = sum(f['quantity_kg'] for f in chemical)
        total_organic = sum(o['quantity_kg'] for o in organic)
        
        if total_chemical + total_organic == 0:
            return 5.0
        
        organic_ratio = total_organic / (total_chemical + total_organic)
        score = 3 + (organic_ratio * 7)  # Base 3, up to 10
        
        return round(score, 1)
    
    def _get_weather_advice(self, weather, schedule):
        """Weather-based application advice"""
        advice = {
            'rain': 'Heavy rain expected. Postpone fertilizer application by 2-3 days to avoid nutrient leaching.',
            'drought': 'Dry conditions. Ensure adequate irrigation before and after fertilizer application.',
            'hot': 'High temperature. Apply fertilizers during early morning or evening to reduce volatilization.',
            'normal': 'Weather conditions are favorable for fertilizer application.'
        }
        return advice.get(weather, advice['normal'])
    
    def _generate_summary(self, crop_type, area_ha, deficiencies, cost):
        """Generate farmer-friendly summary"""
        return {
            'crop': crop_type.title(),
            'area': f"{area_ha:.2f} hectares",
            'deficiencies_found': len(deficiencies),
            'total_cost': f"₹{cost['chemical_total']:.2f}",
            'recommendation': 'Apply fertilizers as per schedule for best results'
        }
