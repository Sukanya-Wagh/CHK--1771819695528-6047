from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import fertilizer_views as fert_views
from . import chatbot_views

urlpatterns = [
    # Home and auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Farm management
    path('farms/', views.farm_list, name='farm_list'),
    path('farms/create/', views.farm_create, name='farm_create'),
    path('farms/<int:farm_id>/analytics/', views.farm_analytics, name='farm_analytics'),
    
    # Crop Health Monitoring (Disease features)
    path('disease/', views.disease_dashboard, name='disease_dashboard'),
    path('disease/report/', views.disease_report_create, name='disease_report_create'),
    path('disease/map/', views.disease_map, name='disease_map'),
    
    # Companion planting
    path('companion-planting/', views.companion_planting, name='companion_planting'),
    
    # Crop & Fertilizer Advisor
    path('crop-advisor/', views.crop_fertilizer_advisor, name='crop_advisor'),
    
    # Crop Planning
    path('crop-planning/', views.crop_planning, name='crop_planning'),
    path('crop-planning/<int:plan_id>/', views.crop_plan_detail, name='crop_plan_detail'),
    
    # API endpoints
    path('api/predict-disease/', views.predict_disease_risk, name='predict_disease_risk'),
    
    # Fertilizer Management System
    path('fertilizer/', fert_views.fertilizer_dashboard, name='fertilizer_dashboard'),
    path('fertilizer/recommendation/', fert_views.fertilizer_recommendation, name='fertilizer_recommendation'),
    path('fertilizer/quantity/', fert_views.fertilizer_quantity_calculator, name='fertilizer_quantity'),
    path('fertilizer/deficiency/', fert_views.nutrient_deficiency_detection, name='nutrient_deficiency'),
    path('fertilizer/schedule/', fert_views.fertilizer_schedule, name='fertilizer_schedule'),
    path('fertilizer/organic/', fert_views.organic_fertilizer_suggestion, name='organic_fertilizer'),
    path('fertilizer/soil-analysis/', fert_views.soil_nutrient_analysis, name='soil_analysis'),
    path('fertilizer/weather-advice/', fert_views.weather_fertilizer_advice, name='weather_fertilizer'),
    
    # AI Chatbot
    path('chatbot/', chatbot_views.chatbot_page, name='chatbot'),
    path('api/chatbot/', chatbot_views.chatbot_api, name='chatbot_api'),
    path('api/chatbot/feedback/', chatbot_views.chatbot_feedback, name='chatbot_feedback'),
    path('api/chatbot/history/', chatbot_views.chatbot_history, name='chatbot_history'),
    path('api/chatbot/clear/', chatbot_views.clear_chat_history, name='clear_chat_history'),
]
