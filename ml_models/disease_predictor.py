import random
import json
from django.conf import settings
from PIL import Image
import io
from datetime import datetime, timedelta

class DiseasePredictor:
    def __init__(self):
        self.disease_classes = [
            'healthy', 'fungal_blight', 'bacterial_spot', 
            'viral_mosaic', 'nutrient_deficiency', 'pest_damage'
        ]
        
        self.pest_types = {
            'aphids': {
                'severity_multiplier': 1.2, 
                'treatment_chemical': 'Imidacloprid 17.8% SL @ 0.5ml/L',
                'treatment_organic': 'Neem oil spray @ 5ml/L + Yellow sticky traps',
                'description': 'Small soft-bodied insects that suck plant sap'
            },
            'whiteflies': {
                'severity_multiplier': 1.3, 
                'treatment_chemical': 'Thiamethoxam 25% WG @ 0.2g/L',
                'treatment_organic': 'Neem oil + Garlic extract spray',
                'description': 'Tiny white flying insects causing leaf yellowing'
            },
            'caterpillars': {
                'severity_multiplier': 1.5, 
                'treatment_chemical': 'Chlorantraniliprole 18.5% SC @ 0.3ml/L',
                'treatment_organic': 'Bacillus thuringiensis (Bt) @ 1g/L',
                'description': 'Larvae that chew leaves and bore into stems'
            },
            'thrips': {
                'severity_multiplier': 1.1, 
                'treatment_chemical': 'Fipronil 5% SC @ 2ml/L',
                'treatment_organic': 'Spinosad-based spray @ 1ml/L',
                'description': 'Tiny insects causing silvering of leaves'
            },
            'mites': {
                'severity_multiplier': 1.4, 
                'treatment_chemical': 'Propargite 57% EC @ 2ml/L',
                'treatment_organic': 'Sulfur dust @ 3g/L water spray',
                'description': 'Spider mites causing leaf bronzing and webbing'
            },
        }
        
        self.nutrient_deficiencies = {
            'nitrogen': {
                'symptoms': 'Yellowing of older leaves, stunted growth',
                'treatment_chemical': 'Urea (46% N) @ 10kg/acre',
                'treatment_organic': 'Vermicompost @ 500kg/acre + Green manure',
                'visual_signs': ['pale_green_leaves', 'yellow_older_leaves', 'slow_growth']
            },
            'phosphorus': {
                'symptoms': 'Purple/dark green leaves, poor root development',
                'treatment_chemical': 'Single Super Phosphate (SSP) @ 15kg/acre',
                'treatment_organic': 'Bone meal @ 50kg/acre + Rock phosphate',
                'visual_signs': ['purple_tint', 'dark_green', 'small_leaves']
            },
            'potassium': {
                'symptoms': 'Brown leaf edges, weak stems',
                'treatment_chemical': 'Muriate of Potash (MOP) @ 8kg/acre',
                'treatment_organic': 'Wood ash @ 100kg/acre + Banana peel compost',
                'visual_signs': ['brown_edges', 'scorched_tips', 'weak_stems']
            },
            'iron': {
                'symptoms': 'Yellowing between veins (interveinal chlorosis)',
                'treatment_chemical': 'Ferrous Sulfate @ 5g/L foliar spray',
                'treatment_organic': 'Iron chelate spray @ 2g/L',
                'visual_signs': ['yellow_veins_green', 'new_leaf_chlorosis']
            },
            'magnesium': {
                'symptoms': 'Interveinal chlorosis in older leaves',
                'treatment_chemical': 'Magnesium Sulfate @ 10g/L spray',
                'treatment_organic': 'Epsom salt solution @ 10g/L',
                'visual_signs': ['interveinal_yellow', 'leaf_curling']
            },
            'zinc': {
                'symptoms': 'Small leaves, short internodes, rosetting',
                'treatment_chemical': 'Zinc Sulfate @ 5g/L foliar spray',
                'treatment_organic': 'Zinc chelate @ 2g/L spray',
                'visual_signs': ['small_leaves', 'rosetting', 'short_internodes']
            },
        }
        
        self.disease_info = {
            'fungal_blight': {
                'name': 'Fungal Blight',
                'cause': 'High humidity and poor air circulation',
                'treatment_chemical': 'Mancozeb 75% WP @ 2g/L or Copper Oxychloride @ 3g/L',
                'treatment_organic': 'Neem cake powder @ 100g/plant + Trichoderma spray',
                'prevention': [
                    'Maintain proper air circulation between plants',
                    'Avoid overhead watering, use drip irrigation',
                    'Remove infected leaves immediately and destroy',
                    'Apply preventive fungicide sprays every 10-15 days'
                ],
                'severity_indicators': ['leaf_spots', 'wilting', 'discoloration'],
                'spread_rate': 'high'
            },
            'bacterial_spot': {
                'name': 'Bacterial Spot',
                'cause': 'High temperature and water splash',
                'treatment_chemical': 'Streptocycline @ 0.5g/L + Copper Oxychloride @ 3g/L',
                'treatment_organic': 'Copper-based bactericide (organic) @ 2ml/L',
                'prevention': [
                    'Use drip irrigation instead of overhead watering',
                    'Increase plant spacing for better air flow',
                    'Remove infected plant parts immediately',
                    'Use disease-resistant varieties'
                ],
                'severity_indicators': ['water_soaked_spots', 'leaf_drop', 'stem_lesions'],
                'spread_rate': 'medium'
            },
            'viral_mosaic': {
                'name': 'Viral Mosaic',
                'cause': 'Insect vectors (aphids, whiteflies)',
                'treatment_chemical': 'No direct cure - Control vectors with Imidacloprid',
                'treatment_organic': 'Remove infected plants + Neem oil for vector control',
                'prevention': [
                    'Control insect vectors with regular monitoring',
                    'Use virus-resistant varieties',
                    'Sanitize tools between plants',
                    'Remove weeds that harbor insects'
                ],
                'severity_indicators': ['mosaic_pattern', 'stunted_growth', 'leaf_curling'],
                'spread_rate': 'high'
            },
            'nutrient_deficiency': {
                'name': 'Nutrient Deficiency',
                'cause': 'Imbalanced soil pH or nutrient levels',
                'treatment_chemical': 'NPK 19:19:19 @ 5g/L foliar spray',
                'treatment_organic': 'Vermicompost @ 500kg/acre + Biofertilizers',
                'prevention': [
                    'Test soil regularly (every 6 months)',
                    'Maintain optimal soil pH (6.0-7.0)',
                    'Apply balanced fertilizers based on soil test',
                    'Use organic compost regularly'
                ],
                'severity_indicators': ['chlorosis', 'necrosis', 'poor_growth'],
                'spread_rate': 'low'
            },
            'pest_damage': {
                'name': 'Pest Damage',
                'cause': 'Insect infestation',
                'treatment_chemical': 'Chlorpyrifos 20% EC @ 2ml/L',
                'treatment_organic': 'Neem-based pesticide @ 5ml/L + Pheromone traps',
                'prevention': [
                    'Regular crop monitoring (twice weekly)',
                    'Use pheromone traps for early detection',
                    'Introduce beneficial insects (ladybugs, lacewings)',
                    'Practice crop rotation'
                ],
                'severity_indicators': ['holes_in_leaves', 'chewed_edges', 'visible_insects'],
                'spread_rate': 'medium'
            },
            'healthy': {
                'name': 'Healthy Crop',
                'cause': 'Good agricultural practices',
                'treatment_chemical': 'No treatment needed',
                'treatment_organic': 'Continue preventive care',
                'prevention': [
                    'Continue current practices',
                    'Monitor regularly for early detection',
                    'Maintain good field hygiene',
                    'Keep detailed crop records'
                ],
                'severity_indicators': [],
                'spread_rate': 'none'
            }
        }
    
    def analyze_leaf_image(self, image_file):
        """Comprehensive leaf image analysis"""
        try:
            img = Image.open(image_file)
            width, height = img.size
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = list(img.getdata())
            
            # Calculate color statistics
            r_avg = sum([p[0] for p in pixels]) / len(pixels)
            g_avg = sum([p[1] for p in pixels]) / len(pixels)
            b_avg = sum([p[2] for p in pixels]) / len(pixels)
            
            # Advanced analysis
            analysis = {
                'image_size': f"{width}x{height}",
                'avg_red': r_avg,
                'avg_green': g_avg,
                'avg_blue': b_avg,
                'has_spots': r_avg < 100 or b_avg > 150,
                'is_yellow': r_avg > 200 and g_avg > 200 and b_avg < 150,
                'is_brown': r_avg > 100 and g_avg < 100 and b_avg < 100,
                'leaf_damage_percent': self._calculate_damage_percent(r_avg, g_avg, b_avg),
                'color_uniformity': self._calculate_uniformity(pixels),
                'health_indicators': self._get_health_indicators(r_avg, g_avg, b_avg)
            }
            
            return analysis
        except Exception as e:
            print(f"Image analysis error: {e}")
            return None
    
    def _calculate_damage_percent(self, r, g, b):
        """Calculate estimated damage percentage"""
        green_health = g / 255.0
        if green_health > 0.6:
            return random.randint(0, 15)
        elif green_health > 0.4:
            return random.randint(15, 40)
        else:
            return random.randint(40, 70)
    
    def _calculate_uniformity(self, pixels):
        """Calculate color uniformity score"""
        if len(pixels) < 100:
            return 0.5
        sample = random.sample(pixels, min(100, len(pixels)))
        r_std = sum([(p[0] - sum([x[0] for x in sample])/len(sample))**2 for p in sample]) / len(sample)
        return max(0, min(1, 1 - (r_std / 10000)))
    
    def _get_health_indicators(self, r, g, b):
        """Get health indicators from color analysis"""
        indicators = []
        if g > 150 and r < 150 and b < 150:
            indicators.append('healthy_green_color')
        if r > 200 and g > 200:
            indicators.append('possible_chlorosis')
        if r > 150 and g < 100 and b < 100:
            indicators.append('browning_detected')
        if b > 150:
            indicators.append('unusual_coloration')
        return indicators
    
    def detect_pests(self, temperature, humidity, image_analysis=None):
        """Detect pest presence, type, and severity with treatment options"""
        pest_detections = []
        
        # Environmental pest risk
        if temperature > 30 and humidity > 60:
            pest_detections.append({
                'pest_type': 'aphids',
                'intensity': 'high' if temperature > 35 else 'medium',
                'confidence': min(85, 60 + (temperature - 30) * 3),
                'treatment_chemical': self.pest_types['aphids']['treatment_chemical'],
                'treatment_organic': self.pest_types['aphids']['treatment_organic'],
                'description': self.pest_types['aphids']['description'],
                'affected_area_estimate': random.randint(20, 40) if temperature > 35 else random.randint(10, 25)
            })
        
        if temperature > 28 and humidity < 50:
            pest_detections.append({
                'pest_type': 'thrips',
                'intensity': 'medium',
                'confidence': min(70, 40 + (temperature - 28) * 5),
                'treatment_chemical': self.pest_types['thrips']['treatment_chemical'],
                'treatment_organic': self.pest_types['thrips']['treatment_organic'],
                'description': self.pest_types['thrips']['description'],
                'affected_area_estimate': random.randint(5, 15)
            })
        
        if image_analysis and image_analysis.get('is_brown'):
            pest_detections.append({
                'pest_type': 'caterpillars',
                'intensity': 'high',
                'confidence': 75,
                'treatment_chemical': self.pest_types['caterpillars']['treatment_chemical'],
                'treatment_organic': self.pest_types['caterpillars']['treatment_organic'],
                'description': self.pest_types['caterpillars']['description'],
                'affected_area_estimate': random.randint(15, 30)
            })
        
        if humidity > 70 and temperature > 25:
            pest_detections.append({
                'pest_type': 'whiteflies',
                'intensity': 'medium',
                'confidence': min(65, 45 + (humidity - 70) * 2),
                'treatment_chemical': self.pest_types['whiteflies']['treatment_chemical'],
                'treatment_organic': self.pest_types['whiteflies']['treatment_organic'],
                'description': self.pest_types['whiteflies']['description'],
                'affected_area_estimate': random.randint(10, 20)
            })
        
        return pest_detections if pest_detections else [{
            'pest_type': 'none',
            'intensity': 'low',
            'confidence': 95,
            'treatment_chemical': 'No treatment needed',
            'treatment_organic': 'Continue monitoring',
            'description': 'No significant pest activity detected',
            'affected_area_estimate': 0
        }]
    
    def analyze_disease_severity(self, confidence, affected_area, image_analysis=None):
        """Analyze disease severity level"""
        severity_score = 0
        
        # Base severity from confidence
        severity_score += confidence * 0.4
        
        # Add affected area impact
        severity_score += affected_area * 0.3
        
        # Image-based severity
        if image_analysis:
            damage_percent = image_analysis.get('leaf_damage_percent', 0)
            severity_score += damage_percent * 0.3
        
        # Classify severity
        if severity_score > 70:
            severity = 'severe'
            action = 'immediate'
            impact = 'Crop yield may reduce by 40-60%'
        elif severity_score > 40:
            severity = 'moderate'
            action = 'within_24_hours'
            impact = 'Crop yield may reduce by 20-40%'
        else:
            severity = 'mild'
            action = 'within_week'
            impact = 'Minimal impact if treated promptly'
        
        return {
            'severity': severity,
            'severity_score': round(severity_score, 1),
            'action_required': action,
            'potential_impact': impact,
            'treatment_priority': 'high' if severity == 'severe' else 'medium' if severity == 'moderate' else 'low'
        }
    
    def calculate_crop_health_score(self, risk_scores, image_analysis=None):
        """Calculate overall crop health score (0-100)"""
        # Start with base health
        health_score = 100
        
        # Deduct for disease risks
        for disease, risk in risk_scores.items():
            if disease != 'healthy':
                health_score -= (risk * 0.15)
        
        # Image-based adjustments
        if image_analysis:
            damage = image_analysis.get('leaf_damage_percent', 0)
            health_score -= (damage * 0.3)
            
            uniformity = image_analysis.get('color_uniformity', 1)
            health_score -= ((1 - uniformity) * 10)
        
        health_score = max(0, min(100, health_score))
        
        # Classify health status
        if health_score >= 80:
            status = 'excellent'
            color = 'success'
        elif health_score >= 60:
            status = 'good'
            color = 'info'
        elif health_score >= 40:
            status = 'fair'
            color = 'warning'
        else:
            status = 'poor'
            color = 'danger'
        
        return {
            'score': round(health_score, 1),
            'status': status,
            'color': color,
            'indicators': self._get_health_status_indicators(health_score)
        }
    
    def _get_health_status_indicators(self, score):
        """Get health status indicators"""
        indicators = []
        if score >= 80:
            indicators = ['Strong growth', 'Good color', 'No visible stress']
        elif score >= 60:
            indicators = ['Moderate growth', 'Some discoloration', 'Minor stress signs']
        elif score >= 40:
            indicators = ['Slow growth', 'Visible damage', 'Stress evident']
        else:
            indicators = ['Poor growth', 'Severe damage', 'Critical condition']
        return indicators
    
    def detect_nutrient_deficiency(self, soil_ph, image_analysis=None):
        """Detect specific nutrient deficiencies with detailed treatment"""
        deficiencies = []
        
        # pH-based detection
        if soil_ph < 6.0:
            deficiencies.append({
                'nutrient': 'phosphorus',
                'likelihood': 'high',
                'symptoms': self.nutrient_deficiencies['phosphorus']['symptoms'],
                'treatment_chemical': self.nutrient_deficiencies['phosphorus']['treatment_chemical'],
                'treatment_organic': self.nutrient_deficiencies['phosphorus']['treatment_organic'],
                'visual_signs': self.nutrient_deficiencies['phosphorus']['visual_signs']
            })
        
        if soil_ph > 7.5:
            deficiencies.append({
                'nutrient': 'iron',
                'likelihood': 'high',
                'symptoms': self.nutrient_deficiencies['iron']['symptoms'],
                'treatment_chemical': self.nutrient_deficiencies['iron']['treatment_chemical'],
                'treatment_organic': self.nutrient_deficiencies['iron']['treatment_organic'],
                'visual_signs': self.nutrient_deficiencies['iron']['visual_signs']
            })
            deficiencies.append({
                'nutrient': 'zinc',
                'likelihood': 'medium',
                'symptoms': self.nutrient_deficiencies['zinc']['symptoms'],
                'treatment_chemical': self.nutrient_deficiencies['zinc']['treatment_chemical'],
                'treatment_organic': self.nutrient_deficiencies['zinc']['treatment_organic'],
                'visual_signs': self.nutrient_deficiencies['zinc']['visual_signs']
            })
        
        # Image-based detection
        if image_analysis:
            if image_analysis.get('is_yellow'):
                deficiencies.append({
                    'nutrient': 'nitrogen',
                    'likelihood': 'high',
                    'symptoms': self.nutrient_deficiencies['nitrogen']['symptoms'],
                    'treatment_chemical': self.nutrient_deficiencies['nitrogen']['treatment_chemical'],
                    'treatment_organic': self.nutrient_deficiencies['nitrogen']['treatment_organic'],
                    'visual_signs': self.nutrient_deficiencies['nitrogen']['visual_signs']
                })
            
            if image_analysis.get('has_spots'):
                deficiencies.append({
                    'nutrient': 'potassium',
                    'likelihood': 'medium',
                    'symptoms': self.nutrient_deficiencies['potassium']['symptoms'],
                    'treatment_chemical': self.nutrient_deficiencies['potassium']['treatment_chemical'],
                    'treatment_organic': self.nutrient_deficiencies['potassium']['treatment_organic'],
                    'visual_signs': self.nutrient_deficiencies['potassium']['visual_signs']
                })
        
        return deficiencies if deficiencies else []
    
    def generate_historical_trend(self, current_risk):
        """Generate simulated historical disease trend"""
        trend_data = []
        base_risk = current_risk
        
        for i in range(7, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            risk_variation = random.randint(-15, 15)
            risk = max(5, min(95, base_risk + risk_variation))
            trend_data.append({
                'date': date,
                'risk_level': risk,
                'status': 'high' if risk > 70 else 'medium' if risk > 40 else 'low'
            })
            base_risk = risk
        
        # Add current day
        trend_data.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'risk_level': current_risk,
            'status': 'high' if current_risk > 70 else 'medium' if current_risk > 40 else 'low'
        })
        
        return trend_data
    
    def get_early_warning_alerts(self, prediction_result, weather_forecast=None):
        """Generate early warning alerts with actionable recommendations"""
        alerts = []
        
        # Critical disease alerts
        if prediction_result['overall_risk'] == 'high':
            alerts.append({
                'type': 'critical',
                'icon': 'exclamation-triangle',
                'message': f"CRITICAL: High risk of {prediction_result['disease_name']} detected!",
                'action': f"Apply {prediction_result['treatment_chemical']} immediately",
                'priority': 1
            })
        
        # Severity-based alerts
        if prediction_result['severity_analysis']['severity'] == 'severe':
            alerts.append({
                'type': 'critical',
                'icon': 'fire',
                'message': f"Severe infection detected - {prediction_result['affected_area']}% area affected",
                'action': prediction_result['severity_analysis']['potential_impact'],
                'priority': 1
            })
        
        # Pest alerts
        if prediction_result.get('pest_detections'):
            for pest in prediction_result['pest_detections']:
                if pest['intensity'] == 'high' and pest['pest_type'] != 'none':
                    alerts.append({
                        'type': 'critical',
                        'icon': 'bug',
                        'message': f"HIGH ALERT: {pest['pest_type'].title()} infestation detected ({pest['confidence']}% confidence)",
                        'action': f"Chemical: {pest['treatment_chemical']} OR Organic: {pest['treatment_organic']}",
                        'priority': 1
                    })
                elif pest['intensity'] == 'medium' and pest['pest_type'] != 'none':
                    alerts.append({
                        'type': 'warning',
                        'icon': 'bug',
                        'message': f"{pest['pest_type'].title()} detected - Monitor closely",
                        'action': pest['treatment_organic'],
                        'priority': 2
                    })
        
        # Nutrient deficiency alerts
        if prediction_result.get('nutrient_deficiencies'):
            for deficiency in prediction_result['nutrient_deficiencies']:
                if deficiency['likelihood'] == 'high':
                    alerts.append({
                        'type': 'warning',
                        'icon': 'flask',
                        'message': f"{deficiency['nutrient'].upper()} deficiency detected - {deficiency['symptoms']}",
                        'action': f"Apply: {deficiency['treatment_chemical']}",
                        'priority': 2
                    })
                else:
                    alerts.append({
                        'type': 'info',
                        'icon': 'info-circle',
                        'message': f"Possible {deficiency['nutrient']} deficiency",
                        'action': deficiency['treatment_organic'],
                        'priority': 3
                    })
        
        # Spread rate warning
        if prediction_result.get('spread_rate') == 'high':
            alerts.append({
                'type': 'warning',
                'icon': 'exclamation-circle',
                'message': f"{prediction_result['disease_name']} spreads rapidly!",
                'action': 'Isolate affected plants and treat neighboring plants preventively',
                'priority': 1
            })
        
        # Sort by priority
        alerts.sort(key=lambda x: x['priority'])
        
        return alerts
    
    def predict_disease_risk(self, temperature, humidity, rainfall, soil_ph, crop_age_days, image_analysis=None):
        """Comprehensive disease prediction with all features"""
        
        # Calculate risk scores
        risk_scores = {}
        
        # Fungal risk
        fungal_risk = 0
        if humidity > 80 and temperature > 25 and rainfall > 5:
            fungal_risk = min(95, 60 + (humidity - 80) * 2 + (rainfall - 5) * 5)
        elif humidity > 70:
            fungal_risk = min(70, 30 + (humidity - 70) * 2)
        else:
            fungal_risk = max(5, 20 - humidity * 0.2)
        
        # Bacterial risk
        bacterial_risk = 0
        if temperature > 30 and humidity < 40:
            bacterial_risk = min(90, 50 + (temperature - 30) * 4)
        elif temperature > 25:
            bacterial_risk = min(60, 20 + (temperature - 25) * 3)
        else:
            bacterial_risk = max(5, 15 - temperature * 0.3)
        
        # Viral risk
        viral_risk = max(5, min(50, 20 + random.randint(-10, 20)))
        
        # Nutrient risk
        nutrient_risk = 0
        if soil_ph < 6 or soil_ph > 8:
            nutrient_risk = min(80, 40 + abs(soil_ph - 7) * 20)
        else:
            nutrient_risk = max(5, 15 - abs(soil_ph - 7) * 5)
        
        # Pest risk
        pest_risk = 0
        if temperature > 35:
            pest_risk = min(75, 30 + (temperature - 35) * 8)
        elif temperature > 25:
            pest_risk = min(40, 10 + (temperature - 25) * 2)
        else:
            pest_risk = max(5, 20 - temperature * 0.5)
        
        # Adjust based on image analysis
        if image_analysis:
            if image_analysis.get('has_spots'):
                fungal_risk = min(95, fungal_risk + 20)
                bacterial_risk = min(90, bacterial_risk + 15)
            if image_analysis.get('is_yellow'):
                nutrient_risk = min(85, nutrient_risk + 25)
            if image_analysis.get('is_brown'):
                pest_risk = min(80, pest_risk + 20)
        
        # Calculate healthy probability
        max_disease_risk = max(fungal_risk, bacterial_risk, viral_risk, nutrient_risk, pest_risk)
        healthy_risk = max(5, 100 - max_disease_risk * 1.2)
        
        risk_scores = {
            'healthy': healthy_risk,
            'fungal_blight': fungal_risk,
            'bacterial_spot': bacterial_risk,
            'viral_mosaic': viral_risk,
            'nutrient_deficiency': nutrient_risk,
            'pest_damage': pest_risk
        }
        
        # Find predicted condition
        predicted_condition = max(risk_scores.items(), key=lambda x: x[1])[0]
        confidence = risk_scores[predicted_condition]
        
        # Calculate affected area
        if confidence > 70:
            affected_area = random.randint(40, 60)
        elif confidence > 40:
            affected_area = random.randint(20, 40)
        else:
            affected_area = random.randint(5, 20)
        
        # Get disease info
        disease_data = self.disease_info.get(predicted_condition, {})
        
        # NEW FEATURES
        # Pest detection
        pest_detections = self.detect_pests(temperature, humidity, image_analysis)
        
        # Disease severity analysis
        severity_analysis = self.analyze_disease_severity(confidence, affected_area, image_analysis)
        
        # Crop health score
        health_score = self.calculate_crop_health_score(risk_scores, image_analysis)
        
        # Nutrient deficiency detection
        nutrient_deficiencies = self.detect_nutrient_deficiency(soil_ph, image_analysis)
        
        # Historical trend
        historical_trend = self.generate_historical_trend(confidence)
        
        # Treatment recommendations
        treatment_plan = self.generate_treatment_plan(
            predicted_condition, 
            disease_data, 
            pest_detections, 
            nutrient_deficiencies,
            severity_analysis
        )
        
        # Comprehensive result
        result = {
            'predicted_condition': predicted_condition,
            'disease_name': disease_data.get('name', 'Unknown'),
            'confidence': round(confidence, 1),
            'risk_scores': {k: round(v, 1) for k, v in risk_scores.items()},
            'overall_risk': self.calculate_overall_risk(risk_scores),
            'affected_area': affected_area,
            'disease_cause': disease_data.get('cause', 'Unknown cause'),
            'treatment_chemical': disease_data.get('treatment_chemical', 'Consult expert'),
            'treatment_organic': disease_data.get('treatment_organic', 'Consult expert'),
            'prevention': disease_data.get('prevention', []),
            'image_analyzed': image_analysis is not None,
            'spread_rate': disease_data.get('spread_rate', 'unknown'),
            
            # NEW FEATURES
            'pest_detections': pest_detections,
            'severity_analysis': severity_analysis,
            'health_score': health_score,
            'nutrient_deficiencies': nutrient_deficiencies,
            'historical_trend': historical_trend,
            'treatment_plan': treatment_plan,
            'leaf_damage_analysis': {
                'damage_percent': image_analysis.get('leaf_damage_percent', 0) if image_analysis else 0,
                'color_uniformity': image_analysis.get('color_uniformity', 1) if image_analysis else 1,
                'health_indicators': image_analysis.get('health_indicators', []) if image_analysis else []
            }
        }
        
        # Generate early warning alerts
        result['early_warnings'] = self.get_early_warning_alerts(result)
        
        # Generate AI recommendations for each category
        result['ai_recommendations'] = self.generate_ai_recommendations(result, predicted_condition, severity_analysis)
        
        return result
    
    def generate_ai_recommendations(self, result, condition, severity_analysis):
        """Generate AI-powered recommendations for each category"""
        recommendations = {
            'disease': [],
            'pest': [],
            'health': [],
            'nutrient': []
        }
        
        # Disease Recommendations
        if condition != 'healthy':
            if severity_analysis['severity'] == 'severe':
                recommendations['disease'].append({
                    'priority': 'critical',
                    'icon': 'exclamation-triangle',
                    'text': f"Immediate action required! Apply {result['treatment_chemical']} within 24 hours to prevent further spread."
                })
                recommendations['disease'].append({
                    'priority': 'high',
                    'icon': 'trash-alt',
                    'text': "Remove and destroy all severely infected plant parts immediately to prevent disease spread to healthy plants."
                })
            elif severity_analysis['severity'] == 'moderate':
                recommendations['disease'].append({
                    'priority': 'high',
                    'icon': 'spray-can',
                    'text': f"Begin treatment within 2-3 days. Alternate between chemical ({result['treatment_chemical']}) and organic ({result['treatment_organic']}) treatments."
                })
            else:
                recommendations['disease'].append({
                    'priority': 'medium',
                    'icon': 'shield-alt',
                    'text': "Apply preventive measures now to stop disease progression. Focus on improving air circulation and reducing humidity."
                })
            
            recommendations['disease'].append({
                'priority': 'medium',
                'icon': 'eye',
                'text': f"Monitor crop daily for next 7 days. Check for spread to neighboring plants. Disease spreads at {result.get('spread_rate', 'medium')} rate."
            })
            recommendations['disease'].append({
                'priority': 'medium',
                'icon': 'calendar-check',
                'text': "Follow the 4-week treatment schedule provided. Consistency is key for effective disease management."
            })
        else:
            recommendations['disease'].append({
                'priority': 'low',
                'icon': 'check-circle',
                'text': "Crop is healthy! Continue current practices and maintain regular monitoring to catch any issues early."
            })
        
        # Pest Recommendations
        if result.get('pest_detections'):
            high_intensity_pests = [p for p in result['pest_detections'] if p['intensity'] == 'high' and p['pest_type'] != 'none']
            if high_intensity_pests:
                recommendations['pest'].append({
                    'priority': 'critical',
                    'icon': 'bug',
                    'text': f"High pest infestation detected! Apply {high_intensity_pests[0]['treatment_chemical']} immediately in evening hours for maximum effectiveness."
                })
                recommendations['pest'].append({
                    'priority': 'high',
                    'icon': 'sticky-note',
                    'text': "Install yellow sticky traps around affected area to monitor and reduce pest population. Replace traps every 7 days."
                })
            
            for pest in result['pest_detections']:
                if pest['pest_type'] != 'none' and pest['intensity'] in ['medium', 'high']:
                    recommendations['pest'].append({
                        'priority': 'medium',
                        'icon': 'leaf',
                        'text': f"For {pest['pest_type']}: {pest['description']}. Organic option: {pest['treatment_organic']}"
                    })
            
            recommendations['pest'].append({
                'priority': 'medium',
                'icon': 'users',
                'text': "Introduce beneficial insects like ladybugs and lacewings to naturally control pest population."
            })
            recommendations['pest'].append({
                'priority': 'low',
                'icon': 'recycle',
                'text': "Practice crop rotation next season to break pest life cycles and reduce future infestations."
            })
        else:
            recommendations['pest'].append({
                'priority': 'low',
                'icon': 'check-circle',
                'text': "No significant pest activity detected. Continue preventive monitoring twice weekly."
            })
        
        # Health Recommendations
        health_score = result['health_score']['score']
        if health_score < 40:
            recommendations['health'].append({
                'priority': 'critical',
                'icon': 'heartbeat',
                'text': "Critical health status! Immediate intervention needed. Consider consulting agricultural expert for comprehensive treatment plan."
            })
            recommendations['health'].append({
                'priority': 'high',
                'icon': 'tint',
                'text': "Check irrigation system immediately. Ensure adequate water supply without waterlogging. Adjust based on soil moisture levels."
            })
        elif health_score < 60:
            recommendations['health'].append({
                'priority': 'high',
                'icon': 'chart-line',
                'text': "Health declining. Address identified issues (disease/pest/nutrients) promptly to prevent further deterioration."
            })
            recommendations['health'].append({
                'priority': 'medium',
                'icon': 'sun',
                'text': "Ensure crop receives adequate sunlight (6-8 hours daily). Prune overcrowded areas to improve light penetration."
            })
        elif health_score < 80:
            recommendations['health'].append({
                'priority': 'medium',
                'icon': 'thumbs-up',
                'text': "Good health status. Minor improvements needed. Focus on preventive care and regular monitoring."
            })
        else:
            recommendations['health'].append({
                'priority': 'low',
                'icon': 'star',
                'text': "Excellent health! Your crop management practices are working well. Maintain current routine."
            })
        
        damage_percent = result['leaf_damage_analysis']['damage_percent']
        if damage_percent > 30:
            recommendations['health'].append({
                'priority': 'high',
                'icon': 'cut',
                'text': f"High leaf damage ({damage_percent}%). Remove damaged leaves to redirect plant energy to healthy growth."
            })
        
        recommendations['health'].append({
            'priority': 'medium',
            'icon': 'clipboard-check',
            'text': "Track health score weekly to identify trends. Early detection of decline allows faster intervention."
        })
        recommendations['health'].append({
            'priority': 'low',
            'icon': 'camera',
            'text': "Take photos weekly to visually track crop progress and compare with AI analysis results."
        })
        
        # Nutrient Recommendations
        if result.get('nutrient_deficiencies'):
            high_priority_deficiencies = [d for d in result['nutrient_deficiencies'] if d['likelihood'] == 'high']
            if high_priority_deficiencies:
                recommendations['nutrient'].append({
                    'priority': 'critical',
                    'icon': 'flask',
                    'text': f"Critical nutrient deficiency detected! Apply {high_priority_deficiencies[0]['treatment_chemical']} as foliar spray for quick absorption."
                })
            
            for deficiency in result['nutrient_deficiencies']:
                recommendations['nutrient'].append({
                    'priority': 'high' if deficiency['likelihood'] == 'high' else 'medium',
                    'icon': 'atom',
                    'text': f"{deficiency['nutrient'].upper()} deficiency: {deficiency['symptoms']}. Organic solution: {deficiency['treatment_organic']}"
                })
            
            recommendations['nutrient'].append({
                'priority': 'medium',
                'icon': 'vial',
                'text': "Conduct soil test every 6 months to monitor nutrient levels and adjust fertilization accordingly."
            })
            recommendations['nutrient'].append({
                'priority': 'medium',
                'icon': 'seedling',
                'text': "Apply vermicompost or well-decomposed farmyard manure to improve soil organic matter and nutrient availability."
            })
        else:
            recommendations['nutrient'].append({
                'priority': 'low',
                'icon': 'check-circle',
                'text': "Nutrient levels appear balanced. Continue current fertilization schedule."
            })
        
        # pH-based recommendations
        recommendations['nutrient'].append({
            'priority': 'medium',
            'icon': 'balance-scale',
            'text': "Maintain soil pH between 6.0-7.0 for optimal nutrient uptake. Test pH monthly and adjust as needed."
        })
        recommendations['nutrient'].append({
            'priority': 'low',
            'icon': 'leaf',
            'text': "Use bio-fertilizers (Azotobacter, PSB, KSB) to enhance nutrient availability and improve soil health naturally."
        })
        
        return recommendations
    
    def generate_treatment_plan(self, condition, disease_data, pest_detections, nutrient_deficiencies, severity_analysis):
        """Generate comprehensive treatment plan"""
        plan = {
            'immediate_actions': [],
            'chemical_treatments': [],
            'organic_treatments': [],
            'preventive_measures': [],
            'application_schedule': []
        }
        
        # Immediate actions based on severity
        if severity_analysis['severity'] == 'severe':
            plan['immediate_actions'].append('Isolate affected plants immediately')
            plan['immediate_actions'].append('Remove and destroy severely infected parts')
            plan['immediate_actions'].append('Apply treatment within 24 hours')
        elif severity_analysis['severity'] == 'moderate':
            plan['immediate_actions'].append('Mark affected areas for monitoring')
            plan['immediate_actions'].append('Begin treatment within 2-3 days')
        else:
            plan['immediate_actions'].append('Monitor closely for progression')
            plan['immediate_actions'].append('Apply preventive measures')
        
        # Disease treatments
        if condition != 'healthy':
            plan['chemical_treatments'].append({
                'type': 'Disease Control',
                'product': disease_data.get('treatment_chemical', 'Consult expert'),
                'timing': 'Apply every 7-10 days',
                'duration': '3-4 applications'
            })
            plan['organic_treatments'].append({
                'type': 'Disease Control',
                'product': disease_data.get('treatment_organic', 'Consult expert'),
                'timing': 'Apply every 5-7 days',
                'duration': '4-5 applications'
            })
        
        # Pest treatments
        for pest in pest_detections:
            if pest['pest_type'] != 'none':
                plan['chemical_treatments'].append({
                    'type': f"{pest['pest_type'].title()} Control",
                    'product': pest.get('treatment_chemical', 'Consult expert'),
                    'timing': 'Apply in evening hours',
                    'duration': '2-3 applications at 7-day intervals'
                })
                plan['organic_treatments'].append({
                    'type': f"{pest['pest_type'].title()} Control",
                    'product': pest.get('treatment_organic', 'Consult expert'),
                    'timing': 'Apply in morning/evening',
                    'duration': '3-4 applications at 5-day intervals'
                })
        
        # Nutrient treatments
        for deficiency in nutrient_deficiencies:
            plan['chemical_treatments'].append({
                'type': f"{deficiency['nutrient'].title()} Supplement",
                'product': deficiency.get('treatment_chemical', 'Consult expert'),
                'timing': 'Apply as soil/foliar application',
                'duration': 'Single application, repeat after 15 days if needed'
            })
            plan['organic_treatments'].append({
                'type': f"{deficiency['nutrient'].title()} Supplement",
                'product': deficiency.get('treatment_organic', 'Consult expert'),
                'timing': 'Apply to soil',
                'duration': 'Mix with soil, effects visible in 2-3 weeks'
            })
        
        # Preventive measures
        plan['preventive_measures'] = disease_data.get('prevention', [])
        
        # Application schedule
        today = datetime.now()
        for i in range(4):
            plan['application_schedule'].append({
                'day': (today + timedelta(days=i*7)).strftime('%Y-%m-%d'),
                'week': f"Week {i+1}",
                'action': f"Application {i+1}" if i < 3 else "Final assessment",
                'note': 'Monitor crop response' if i > 0 else 'Initial treatment'
            })
        
        return plan
    
    def calculate_overall_risk(self, risk_scores):
        """Calculate overall disease risk level"""
        max_disease_risk = max([score for disease, score in risk_scores.items() if disease != 'healthy'])
        
        if max_disease_risk > 70:
            return 'high'
        elif max_disease_risk > 40:
            return 'medium'
        else:
            return 'low'
    
    def get_recommendations(self, prediction_result):
        """Get recommendations based on prediction"""
        return prediction_result.get('prevention', [])

# Global instance
disease_predictor = DiseasePredictor()