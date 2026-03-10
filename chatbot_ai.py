"""
AI Chatbot Engine for KrushiRakshak
Intelligent agriculture advisor with context-aware responses
"""

import re
import time
from datetime import datetime
from .models import ChatMessage, AgricultureKnowledgeBase


class AgricultureChatbot:
    """Intelligent chatbot for agriculture queries"""
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self):
        """Load comprehensive agriculture knowledge"""
        return {
            'crop_diseases': {
                'keywords': ['disease', 'infection', 'fungus', 'bacteria', 'virus', 'rot', 'blight', 'wilt', 'spot'],
                'responses': {
                    'rice': {
                        'blast': 'Rice Blast: Caused by fungus. Symptoms: Diamond-shaped lesions on leaves. Treatment: Use Tricyclazole fungicide, maintain proper spacing, avoid excess nitrogen.',
                        'blight': 'Bacterial Blight: Water-soaked lesions. Treatment: Use copper-based bactericides, remove infected plants, use resistant varieties.',
                        'sheath_blight': 'Sheath Blight: Oval lesions on leaf sheaths. Treatment: Apply Validamycin or Hexaconazole, maintain field hygiene.'
                    },
                    'wheat': {
                        'rust': 'Wheat Rust: Orange/brown pustules on leaves. Treatment: Apply Propiconazole, use resistant varieties, timely sowing.',
                        'bunt': 'Wheat Bunt: Grains filled with black powder. Treatment: Seed treatment with Vitavax, use certified seeds.'
                    },
                    'tomato': {
                        'blight': 'Late Blight: Dark lesions on leaves and fruits. Treatment: Apply Mancozeb or Metalaxyl, improve air circulation.',
                        'wilt': 'Bacterial Wilt: Sudden wilting. Treatment: Remove infected plants, crop rotation, use resistant varieties.'
                    },
                    'cotton': {
                        'wilt': 'Cotton Wilt: Yellowing and wilting. Treatment: Seed treatment, crop rotation, use resistant varieties.',
                        'boll_rot': 'Boll Rot: Rotting of cotton bolls. Treatment: Apply Carbendazim, maintain proper spacing.'
                    }
                }
            },
            'pests': {
                'keywords': ['pest', 'insect', 'worm', 'caterpillar', 'aphid', 'whitefly', 'bollworm', 'borer'],
                'responses': {
                    'rice': 'Common pests: Stem borer, Leaf folder, Brown planthopper. Control: Use Chlorpyrifos, maintain water level, use pheromone traps.',
                    'wheat': 'Common pests: Aphids, Termites. Control: Use Imidacloprid, seed treatment, timely irrigation.',
                    'cotton': 'Common pests: Bollworm, Whitefly, Aphids. Control: Use Bt cotton, spray Emamectin benzoate, install yellow sticky traps.',
                    'tomato': 'Common pests: Fruit borer, Whitefly. Control: Use Spinosad, install pheromone traps, maintain field hygiene.',
                    'general': 'Integrated Pest Management: Use neem oil, install traps, encourage natural predators, rotate crops, maintain field hygiene.'
                }
            },
            'fertilizers': {
                'keywords': ['fertilizer', 'nutrient', 'nitrogen', 'phosphorus', 'potassium', 'npk', 'urea', 'dap', 'manure'],
                'responses': {
                    'rice': 'Rice Fertilizer: Basal - 50kg DAP/ha, 25 DAS - 45kg Urea/ha, 45 DAS - 30kg MOP/ha. Split application recommended.',
                    'wheat': 'Wheat Fertilizer: Basal - 60kg DAP/ha, 21 DAS - 50kg Urea/ha, 60 DAS - 40kg Urea/ha.',
                    'cotton': 'Cotton Fertilizer: Basal - 60kg NPK/ha, 30 DAS - 45kg Urea/ha, 60 DAS - 40kg MOP/ha.',
                    'tomato': 'Tomato Fertilizer: High NPK requirement. Use 150:80:120 kg/ha. Apply in splits with organic manure.',
                    'deficiency': {
                        'nitrogen': 'Nitrogen Deficiency: Yellow leaves, stunted growth. Apply Urea 45-50 kg/ha.',
                        'phosphorus': 'Phosphorus Deficiency: Purple leaves, poor root. Apply DAP 40-50 kg/ha.',
                        'potassium': 'Potassium Deficiency: Brown leaf edges. Apply MOP 30-40 kg/ha.'
                    },
                    'organic': 'Organic Options: Vermicompost (2-3 tons/ha), Neem cake (200kg/ha), FYM (10-15 tons/ha). Improves soil health naturally.'
                }
            },
            'weather': {
                'keywords': ['weather', 'rain', 'temperature', 'humidity', 'drought', 'flood', 'climate'],
                'responses': {
                    'rain': 'Heavy Rain Advisory: Avoid fertilizer application 2-3 days before rain. Ensure proper drainage. Spray fungicides after rain stops.',
                    'drought': 'Drought Management: Use mulching, drip irrigation, drought-resistant varieties. Apply water-retaining polymers.',
                    'heat': 'High Temperature: Irrigate during early morning/evening. Use shade nets for vegetables. Apply potassium for heat tolerance.',
                    'cold': 'Cold Weather: Protect seedlings with covers. Avoid irrigation during frost. Use smoke to prevent frost damage.'
                }
            },
            'crop_care': {
                'keywords': ['care', 'cultivation', 'planting', 'sowing', 'harvest', 'irrigation', 'spacing'],
                'responses': {
                    'rice': 'Rice Cultivation: Transplant 20-25 day seedlings, 20x15cm spacing, maintain 5cm water level, harvest at 80% grain maturity.',
                    'wheat': 'Wheat Cultivation: Sow in November, 20cm row spacing, 100kg seed/ha, 4-5 irrigations, harvest when grains harden.',
                    'cotton': 'Cotton Cultivation: Sow in May-June, 90x60cm spacing, regular irrigation, harvest when bolls open fully.',
                    'tomato': 'Tomato Cultivation: Transplant 4-week seedlings, 60x45cm spacing, stake plants, regular irrigation, harvest when fully colored.'
                }
            },
            'general': {
                'keywords': ['help', 'hello', 'hi', 'thanks', 'thank you', 'bye'],
                'responses': {
                    'greeting': 'Namaste! 🌾 I am KrushiRakshak AI Advisor. I can help you with crop diseases, pests, fertilizers, weather advice, and farming practices. How can I assist you today?',
                    'thanks': 'You\'re welcome! Happy farming! 🌱 Feel free to ask if you have more questions.',
                    'bye': 'Goodbye! May your crops flourish! 🌾 Come back anytime for farming advice.'
                }
            }
        }
    
    def get_response(self, user_message, crop_type=None, season=None):
        """Generate intelligent response based on user query"""
        start_time = time.time()
        
        # Normalize message
        message_lower = user_message.lower().strip()
        
        # Detect query category and generate response
        category, response, confidence = self._analyze_and_respond(message_lower, crop_type, season)
        
        response_time = time.time() - start_time
        
        return {
            'response': response,
            'category': category,
            'confidence': confidence,
            'response_time': response_time,
            'crop_type': crop_type or 'general',
            'season': season or 'all'
        }
    
    def _analyze_and_respond(self, message, crop_type, season):
        """Analyze message and generate appropriate response"""
        
        # Check for greetings
        if any(word in message for word in ['hello', 'hi', 'hey', 'namaste']):
            return 'general', self.knowledge_base['general']['responses']['greeting'], 0.95
        
        if any(word in message for word in ['thank', 'thanks']):
            return 'general', self.knowledge_base['general']['responses']['thanks'], 0.95
        
        if any(word in message for word in ['bye', 'goodbye']):
            return 'general', self.knowledge_base['general']['responses']['bye'], 0.95
        
        # Check for disease queries
        if any(keyword in message for keyword in self.knowledge_base['crop_diseases']['keywords']):
            return self._handle_disease_query(message, crop_type)
        
        # Check for pest queries
        if any(keyword in message for keyword in self.knowledge_base['pests']['keywords']):
            return self._handle_pest_query(message, crop_type)
        
        # Check for fertilizer queries
        if any(keyword in message for keyword in self.knowledge_base['fertilizers']['keywords']):
            return self._handle_fertilizer_query(message, crop_type)
        
        # Check for weather queries
        if any(keyword in message for keyword in self.knowledge_base['weather']['keywords']):
            return self._handle_weather_query(message)
        
        # Check for crop care queries
        if any(keyword in message for keyword in self.knowledge_base['crop_care']['keywords']):
            return self._handle_crop_care_query(message, crop_type)
        
        # Default response
        return 'general', self._get_default_response(), 0.5
    
    def _handle_disease_query(self, message, crop_type):
        """Handle disease-related queries"""
        diseases = self.knowledge_base['crop_diseases']['responses']
        
        if crop_type and crop_type.lower() in diseases:
            crop_diseases = diseases[crop_type.lower()]
            
            # Check for specific disease
            for disease_name, info in crop_diseases.items():
                if disease_name.replace('_', ' ') in message:
                    return 'disease', info, 0.9
            
            # Return general disease info for crop
            response = f"Common {crop_type} diseases:\n\n"
            for disease_name, info in crop_diseases.items():
                response += f"• {info}\n\n"
            return 'disease', response.strip(), 0.8
        
        # General disease advice
        return 'disease', "Please specify your crop type for accurate disease information. Common practices: Remove infected plants, use fungicides, maintain field hygiene, crop rotation.", 0.6
    
    def _handle_pest_query(self, message, crop_type):
        """Handle pest-related queries"""
        pests = self.knowledge_base['pests']['responses']
        
        if crop_type and crop_type.lower() in pests:
            return 'pest', pests[crop_type.lower()], 0.85
        
        return 'pest', pests['general'], 0.7
    
    def _handle_fertilizer_query(self, message, crop_type):
        """Handle fertilizer-related queries"""
        fertilizers = self.knowledge_base['fertilizers']['responses']
        
        # Check for deficiency queries
        if 'deficiency' in message or 'yellow' in message or 'purple' in message:
            if 'nitrogen' in message or 'yellow' in message:
                return 'fertilizer', fertilizers['deficiency']['nitrogen'], 0.85
            elif 'phosphorus' in message or 'purple' in message:
                return 'fertilizer', fertilizers['deficiency']['phosphorus'], 0.85
            elif 'potassium' in message or 'brown' in message:
                return 'fertilizer', fertilizers['deficiency']['potassium'], 0.85
        
        # Check for organic fertilizer
        if 'organic' in message:
            return 'fertilizer', fertilizers['organic'], 0.85
        
        # Crop-specific fertilizer
        if crop_type and crop_type.lower() in fertilizers:
            return 'fertilizer', fertilizers[crop_type.lower()], 0.85
        
        return 'fertilizer', "For accurate fertilizer recommendations, please specify your crop type. General advice: Use balanced NPK, apply in splits, consider soil test results.", 0.6
    
    def _handle_weather_query(self, message):
        """Handle weather-related queries"""
        weather = self.knowledge_base['weather']['responses']
        
        if 'rain' in message:
            return 'weather', weather['rain'], 0.85
        elif 'drought' in message or 'dry' in message:
            return 'weather', weather['drought'], 0.85
        elif 'heat' in message or 'hot' in message or 'temperature' in message:
            return 'weather', weather['heat'], 0.85
        elif 'cold' in message or 'frost' in message:
            return 'weather', weather['cold'], 0.85
        
        return 'weather', "Weather-based farming advice: Monitor forecasts, adjust irrigation, protect crops from extreme weather, apply inputs at optimal times.", 0.7
    
    def _handle_crop_care_query(self, message, crop_type):
        """Handle general crop care queries"""
        care = self.knowledge_base['crop_care']['responses']
        
        if crop_type and crop_type.lower() in care:
            return 'crop_care', care[crop_type.lower()], 0.85
        
        return 'crop_care', "General crop care: Proper spacing, timely irrigation, weed control, pest monitoring, balanced nutrition, timely harvest.", 0.7
    
    def _get_default_response(self):
        """Default response when query is not understood"""
        return """I can help you with:
        
🌾 Crop Diseases - Identification and treatment
🐛 Pest Management - Control measures
💊 Fertilizer Recommendations - NPK and organic options
🌤️ Weather Advice - Farming based on weather
🌱 Crop Care - Cultivation practices

Please ask your question with more details about your crop or farming issue."""
