from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'farms', views.FarmViewSet)
router.register(r'crops', views.CropViewSet)
router.register(r'disease-reports', views.DiseaseReportViewSet)
router.register(r'sensor-data', views.SensorDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict-disease/', views.predict_disease_api, name='predict_disease_api'),
    path('companion-advice/', views.companion_advice_api, name='companion_advice_api'),
    path('research-papers/', views.research_papers_api, name='research_papers_api'),
]