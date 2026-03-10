from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
import json

from core.models import Farm, Crop, DiseaseReport, SensorData
from .serializers import FarmSerializer, CropSerializer, DiseaseReportSerializer, SensorDataSerializer
from ml_models.disease_predictor import disease_predictor
from ml_models.research_matcher import research_matcher

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class DiseaseReportViewSet(viewsets.ModelViewSet):
    queryset = DiseaseReport.objects.all()
    serializer_class = DiseaseReportSerializer

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def predict_disease_api(request):
    """API endpoint for disease prediction"""
    try:
        data = request.data
        
        temperature = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 60))
        rainfall = float(data.get('rainfall', 2))
        soil_ph = float(data.get('soil_ph', 6.5))
        crop_age = int(data.get('crop_age_days', 30))
        
        prediction = disease_predictor.predict_disease_risk(
            temperature, humidity, rainfall, soil_ph, crop_age
        )
        
        recommendations = disease_predictor.get_recommendations(prediction)
        prediction['recommendations'] = recommendations
        
        return Response(prediction, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def companion_advice_api(request):
    """API endpoint for companion planting advice"""
    try:
        data = request.data
        primary_crop = data.get('primary_crop')
        garden_size = data.get('garden_size', 'medium')
        
        if not primary_crop:
            return Response({'error': 'primary_crop is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        recommendations = research_matcher.find_companion_plants(primary_crop, garden_size)
        
        return Response(recommendations, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def research_papers_api(request):
    """API endpoint for research paper search"""
    try:
        query = request.GET.get('query', '')
        crop_type = request.GET.get('crop_type', '')
        
        papers = research_matcher.search_research_papers(query, crop_type)
        
        return Response({'papers': papers}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)