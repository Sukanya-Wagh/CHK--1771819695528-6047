import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import requests
from datetime import datetime, timedelta

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.crop_encodings = {
            'corn': 0, 'tomato': 1, 'wheat': 2, 
            'potato': 3, 'soybean': 4
        }
        
    def generate_training_data(self, n_samples=1000):
        """Generate synthetic training data for disease prediction"""
        np.random.seed(42)
        
        data = []
        for _ in range(n_samples):
            # Weather features
            temp = np.random.normal(75, 15)  # Temperature
            humidity = np.random.normal(65, 20)  # Humidity
            rainfall = np.random.exponential(2)  # Rainfall
            wind_speed = np.random.normal(10, 5)  # Wind speed
            
            # Crop type
            crop = np.random.choice(list(self.crop_encodings.keys()))
            crop_encoded = self.crop_encodings[crop]
            
            # Seasonal factor
            day_of_year = np.random.randint(1, 365)
            season_factor = np.sin(2 * np.pi * day_of_year / 365)
            
            # Calculate disease risk based on conditions
            fungal_risk = self._calculate_fungal_risk(temp, humidity, rainfall)
            bacterial_risk = self._calculate_bacterial_risk(temp, humidity, wind_speed)
            viral_risk = self._calculate_viral_risk(temp, season_factor)
            
            # Overall disease presence (binary)
            disease_present = int(max(fungal_risk, bacterial_risk, viral_risk) > 0.6)
            
            data.append([
                temp, humidity, rainfall, wind_speed, crop_encoded, 
                season_factor, disease_present, fungal_risk, 
                bacterial_risk, viral_risk
            ])
        
        columns = [
            'temperature', 'humidity', 'rainfall', 'wind_speed', 
            'crop_type', 'season_factor', 'disease_present',
            'fungal_risk', 'bacterial_risk', 'viral_risk'
        ]
        
        return pd.DataFrame(data, columns=columns)
    
    def _calculate_fungal_risk(self, temp, humidity, rainfall):
        """Calculate fungal disease risk based on weather"""
        risk = 0
        if humidity > 70:
            risk += 0.3
        if rainfall > 2:
            risk += 0.2
        if 70 <= temp <= 85:
            risk += 0.2
        return min(1.0, risk + np.random.normal(0, 0.1))
    
    def _calculate_bacterial_risk(self, temp, humidity, wind_speed):
        """Calculate bacterial disease risk"""
        risk = 0
        if temp > 80:
            risk += 0.3
        if humidity > 60:
            risk += 0.2
        if wind_speed < 5:  # Low wind = poor air circulation
            risk += 0.1
        return min(1.0, risk + np.random.normal(0, 0.1))
    
    def _calculate_viral_risk(self, temp, season_factor):
        """Calculate viral disease risk"""
        risk = 0
        if temp > 85:
            risk += 0.2
        if season_factor > 0:  # Summer months
            risk += 0.1
        return min(1.0, risk + np.random.normal(0, 0.15))
    
    def train_model(self):
        """Train the disease prediction model"""
        # Generate training data
        df = self.generate_training_data()
        
        # Prepare features and targets
        feature_cols = ['temperature', 'humidity', 'rainfall', 'wind_speed', 
                       'crop_type', 'season_factor']
        X = df[feature_cols]
        y = df['disease_present']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=10
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Calculate accuracy
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"Model accuracy: {accuracy:.3f}")
        
        return accuracy
    
    def predict_disease_risk(self, weather_data, crop_type, location=None):
        """Predict disease risk for given conditions"""
        if self.model is None:
            self.train_model()
        
        # Prepare input data
        crop_encoded = self.crop_encodings.get(crop_type.lower(), 0)
        
        # Calculate season factor
        day_of_year = datetime.now().timetuple().tm_yday
        season_factor = np.sin(2 * np.pi * day_of_year / 365)
        
        # Create feature vector
        features = np.array([[
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['rainfall'],
            weather_data.get('wind_speed', 10),
            crop_encoded,
            season_factor
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        disease_prob = self.model.predict_proba(features_scaled)[0][1]
        
        # Calculate specific disease risks
        fungal_risk = self._calculate_fungal_risk(
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['rainfall']
        ) * 100
        
        bacterial_risk = self._calculate_bacterial_risk(
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data.get('wind_speed', 10)
        ) * 100
        
        viral_risk = self._calculate_viral_risk(
            weather_data['temperature'],
            season_factor
        ) * 100
        
        return {
            'overall_risk': disease_prob * 100,
            'fungal_risk': fungal_risk,
            'bacterial_risk': bacterial_risk,
            'viral_risk': viral_risk,
            'recommendations': self._get_recommendations(disease_prob * 100)
        }
    
    def _get_recommendations(self, risk_level):
        """Get recommendations based on risk level"""
        if risk_level > 70:
            return [
                "Apply preventive fungicides immediately",
                "Increase field monitoring to twice daily",
                "Consider early harvest if disease spreads",
                "Improve drainage in affected areas"
            ]
        elif risk_level > 40:
            return [
                "Increase scouting frequency to daily",
                "Prepare treatment options",
                "Monitor weather conditions closely",
                "Check irrigation systems"
            ]
        else:
            return [
                "Continue normal operations",
                "Maintain regular scouting schedule",
                "Keep treatment options ready"
            ]
    
    def get_weather_data(self, location, api_key=None):
        """Fetch real weather data (mock implementation)"""
        # Mock weather data - in production, use OpenWeatherMap API
        return {
            'temperature': np.random.normal(75, 10),
            'humidity': np.random.normal(65, 15),
            'rainfall': np.random.exponential(2),
            'wind_speed': np.random.normal(10, 5)
        }
    
    def save_model(self, filepath):
        """Save trained model"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'crop_encodings': self.crop_encodings
            }, filepath)
    
    def load_model(self, filepath):
        """Load trained model"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.crop_encodings = data['crop_encodings']

# Example usage
if __name__ == "__main__":
    predictor = DiseasePredictor()
    accuracy = predictor.train_model()
    
    # Test prediction
    weather = {
        'temperature': 78,
        'humidity': 75,
        'rainfall': 3.2,
        'wind_speed': 8
    }
    
    result = predictor.predict_disease_risk(weather, 'tomato')
    print(f"Disease risk prediction: {result}")