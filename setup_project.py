#!/usr/bin/env python
"""
FarmSphere Setup Script
Run this to set up the Django project for the hackathon
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command):
    """Run a shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def setup_django():
    """Set up Django project"""
    print("Setting up Django project...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmsphere.settings')
    django.setup()
    
    # Run migrations
    print("Creating database tables...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser (optional)
    print("Creating superuser...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@farmsphere.com', 'admin123')
            print("Superuser created: admin/admin123")
    except Exception as e:
        print(f"Could not create superuser: {e}")
    
    # Load sample data
    load_sample_data()

def load_sample_data():
    """Load sample data for demo"""
    print("Loading sample data...")
    
    try:
        from django.contrib.auth.models import User
        from core.models import Farm, Crop, ResearchPaper, CompanionPlantingRule
        
        # Create sample user
        if not User.objects.filter(username='farmer1').exists():
            farmer = User.objects.create_user('farmer1', 'farmer1@example.com', 'password123')
            
            # Create sample farm
            farm = Farm.objects.create(
                farmer=farmer,
                name="Green Valley Farm",
                latitude=41.8781,
                longitude=-87.6298,
                size_acres=150,
                address="123 Farm Road, Iowa, USA"
            )
            
            # Create sample crops
            from datetime import date, timedelta
            Crop.objects.create(
                farm=farm,
                crop_type='corn',
                planting_date=date.today() - timedelta(days=60),
                expected_harvest=date.today() + timedelta(days=30),
                area_acres=50,
                health_status='healthy'
            )
            
            Crop.objects.create(
                farm=farm,
                crop_type='tomato',
                planting_date=date.today() - timedelta(days=45),
                expected_harvest=date.today() + timedelta(days=45),
                area_acres=25,
                health_status='at_risk'
            )
        
        # Create sample research papers
        if not ResearchPaper.objects.exists():
            ResearchPaper.objects.create(
                title="Companion Planting Effects on Pest Management in Organic Vegetable Production",
                authors="Smith, J.A., Johnson, M.B., Williams, C.D.",
                abstract="This study examines the effectiveness of companion planting strategies in reducing pest populations and improving crop yields in organic vegetable systems.",
                publication_date=date(2019, 3, 15),
                journal="Journal of Sustainable Agriculture",
                doi="10.1080/10440046.2019.1234567",
                keywords="companion planting, pest management, organic farming, tomato, basil",
                citation_count=127
            )
            
            ResearchPaper.objects.create(
                title="Nitrogen Fixation Benefits in Three Sisters Agriculture Systems",
                authors="Garcia, R.M., Thompson, K.L., Anderson, P.J.",
                abstract="Traditional Three Sisters planting (corn, beans, squash) provides significant nitrogen benefits through biological nitrogen fixation.",
                publication_date=date(2018, 11, 22),
                journal="Agronomy Journal",
                doi="10.2134/agronj2018.05.0312",
                keywords="three sisters, nitrogen fixation, corn, beans, squash, polyculture",
                citation_count=203
            )
        
        # Create companion planting rules
        if not CompanionPlantingRule.objects.exists():
            rules = [
                ('tomato', 'basil', 'beneficial', 'Basil repels aphids and improves tomato flavor', 0.85),
                ('tomato', 'marigold', 'beneficial', 'Marigolds reduce nematode populations', 0.92),
                ('corn', 'beans', 'beneficial', 'Beans fix nitrogen for corn', 0.95),
                ('corn', 'squash', 'beneficial', 'Squash provides ground cover', 0.88),
                ('tomato', 'walnut', 'harmful', 'Walnut produces toxic juglone', 0.98),
            ]
            
            for primary, companion, relationship, benefit, confidence in rules:
                CompanionPlantingRule.objects.create(
                    primary_crop=primary,
                    companion_crop=companion,
                    relationship_type=relationship,
                    benefit_description=benefit,
                    confidence_score=confidence
                )
        
        print("Sample data loaded successfully!")
        
    except Exception as e:
        print(f"Error loading sample data: {e}")

def main():
    """Main setup function"""
    print("🌱 FarmSphere Setup Script")
    print("=" * 50)
    
    # Install requirements
    print("Installing Python packages...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install requirements. Please install manually.")
        return
    
    # Setup Django
    setup_django()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Open: http://127.0.0.1:8000")
    print("3. Login with: admin/admin123 or farmer1/password123")
    print("\nFor the demo:")
    print("- Go to Disease Prediction and try the corn demo")
    print("- Go to Companion Planting and try tomato recommendations")
    print("- Admin panel: http://127.0.0.1:8000/admin")

if __name__ == "__main__":
    main()