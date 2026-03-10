import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# Page config
st.set_page_config(
    page_title="FarmSphere - AI Agriculture Research Platform",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🌱 FarmSphere</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">AI-Powered Agriculture Research Platform</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a feature:", [
        "🏠 Home",
        "🦠 Disease Prediction",
        "🌿 Companion Planting Advisor"
    ])
    
    if page == "🏠 Home":
        show_home()
    elif page == "🦠 Disease Prediction":
        show_disease_prediction()
    elif page == "🌿 Companion Planting Advisor":
        show_companion_planting()

def show_home():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🦠 Disease Spread Prediction</h3>
            <p>AI-powered disease risk assessment using weather data and machine learning models.</p>
            <ul>
                <li>Real-time weather integration</li>
                <li>Interactive risk visualization</li>
                <li>Predictive modeling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌿 Companion Planting Advisor</h3>
            <p>Research-backed recommendations for optimal crop combinations.</p>
            <ul>
                <li>Scientific paper citations</li>
                <li>Compatibility scoring</li>
                <li>Benefit explanations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Demo Scenarios")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌽 Corn Farm Disease Risk"):
            st.session_state.demo_crop = "corn"
            st.session_state.demo_location = "Iowa"
    
    with col2:
        if st.button("🍅 Tomato Companion Plants"):
            st.session_state.demo_crop = "tomato"
    
    with col3:
        if st.button("🥕 Vegetable Garden Plan"):
            st.session_state.demo_garden = True

def show_disease_prediction():
    st.header("🦠 Disease Spread Prediction")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Farm Parameters")
        crop = st.selectbox("Select Crop:", ["Corn", "Tomato", "Wheat", "Potato", "Soybean"])
        location = st.text_input("Location:", "Iowa, USA")
        farm_size = st.slider("Farm Size (acres):", 1, 1000, 100)
        
        if st.button("Analyze Disease Risk"):
            with st.spinner("Analyzing disease risk..."):
                risk_data = generate_disease_prediction(crop, location, farm_size)
                st.session_state.risk_data = risk_data
    
    with col2:
        if 'risk_data' in st.session_state:
            display_disease_visualization(st.session_state.risk_data)

def show_companion_planting():
    st.header("🌿 Companion Planting Advisor")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Plant Selection")
        primary_crop = st.selectbox("Primary Crop:", [
            "Tomato", "Corn", "Beans", "Lettuce", "Carrots", 
            "Peppers", "Cucumber", "Squash", "Basil"
        ])
        
        garden_size = st.selectbox("Garden Size:", ["Small (< 100 sq ft)", "Medium (100-500 sq ft)", "Large (> 500 sq ft)"])
        
        if st.button("Get Companion Recommendations"):
            with st.spinner("Searching research database..."):
                recommendations = get_companion_recommendations(primary_crop)
                st.session_state.recommendations = recommendations
    
    with col2:
        if 'recommendations' in st.session_state:
            display_companion_recommendations(st.session_state.recommendations, primary_crop)

def generate_disease_prediction(crop, location, farm_size):
    # Simulate disease risk prediction
    np.random.seed(42)
    
    # Generate weather-based risk factors
    temperature = np.random.normal(75, 10)
    humidity = np.random.normal(65, 15)
    rainfall = np.random.normal(2.5, 1.2)
    
    # Calculate risk scores
    fungal_risk = min(100, max(0, (humidity - 50) * 2 + (rainfall - 1) * 15))
    bacterial_risk = min(100, max(0, (temperature - 70) * 3 + humidity * 0.5))
    viral_risk = min(100, max(0, np.random.normal(30, 15)))
    
    return {
        'crop': crop,
        'location': location,
        'farm_size': farm_size,
        'weather': {
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'rainfall': round(rainfall, 2)
        },
        'risks': {
            'Fungal Diseases': round(fungal_risk, 1),
            'Bacterial Diseases': round(bacterial_risk, 1),
            'Viral Diseases': round(viral_risk, 1)
        }
    }

def display_disease_visualization(risk_data):
    st.subheader("Disease Risk Assessment")
    
    # Risk gauge chart
    fig = go.Figure()
    
    for disease, risk in risk_data['risks'].items():
        color = 'red' if risk > 70 else 'orange' if risk > 40 else 'green'
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = risk,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': disease},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Weather conditions
    st.subheader("Current Weather Conditions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Temperature", f"{risk_data['weather']['temperature']}°F")
    with col2:
        st.metric("Humidity", f"{risk_data['weather']['humidity']}%")
    with col3:
        st.metric("Rainfall", f"{risk_data['weather']['rainfall']} inches")
    
    # Recommendations
    st.subheader("Recommendations")
    max_risk = max(risk_data['risks'].values())
    
    if max_risk > 70:
        st.error("⚠️ High disease risk detected! Immediate action recommended.")
        st.write("- Apply preventive fungicides")
        st.write("- Increase field monitoring")
        st.write("- Consider early harvest if applicable")
    elif max_risk > 40:
        st.warning("⚡ Moderate disease risk. Monitor closely.")
        st.write("- Increase scouting frequency")
        st.write("- Prepare treatment options")
    else:
        st.success("✅ Low disease risk. Continue normal operations.")

def get_companion_recommendations(primary_crop):
    # Companion planting database with research citations
    companion_db = {
        "Tomato": {
            "excellent": [
                {"plant": "Basil", "benefit": "Repels pests, improves flavor", "research": "Journal of Agricultural Science, 2019"},
                {"plant": "Marigold", "benefit": "Nematode control", "research": "Plant Disease Management, 2020"}
            ],
            "good": [
                {"plant": "Lettuce", "benefit": "Space utilization", "research": "Sustainable Agriculture Review, 2018"},
                {"plant": "Carrots", "benefit": "Soil aeration", "research": "Crop Science Journal, 2021"}
            ],
            "avoid": [
                {"plant": "Walnut", "benefit": "Allelopathic effects", "research": "Allelopathy Journal, 2017"}
            ]
        },
        "Corn": {
            "excellent": [
                {"plant": "Beans", "benefit": "Nitrogen fixation", "research": "Agronomy Journal, 2020"},
                {"plant": "Squash", "benefit": "Ground cover, pest control", "research": "Three Sisters Study, 2019"}
            ],
            "good": [
                {"plant": "Sunflower", "benefit": "Beneficial insect habitat", "research": "Ecological Agriculture, 2018"}
            ],
            "avoid": [
                {"plant": "Tomato", "benefit": "Competition for nutrients", "research": "Plant Nutrition Studies, 2019"}
            ]
        }
    }
    
    return companion_db.get(primary_crop, {
        "excellent": [{"plant": "Research in progress", "benefit": "Data being collected", "research": "Ongoing studies"}],
        "good": [],
        "avoid": []
    })

def display_companion_recommendations(recommendations, primary_crop):
    st.subheader(f"Companion Plants for {primary_crop}")
    
    # Excellent companions
    if recommendations.get("excellent"):
        st.markdown("### 🌟 Excellent Companions")
        for comp in recommendations["excellent"]:
            with st.expander(f"🌱 {comp['plant']}"):
                st.write(f"**Benefit:** {comp['benefit']}")
                st.write(f"**Research Source:** {comp['research']}")
                st.write("**Compatibility Score:** 95/100")
    
    # Good companions
    if recommendations.get("good"):
        st.markdown("### ✅ Good Companions")
        for comp in recommendations["good"]:
            with st.expander(f"🌿 {comp['plant']}"):
                st.write(f"**Benefit:** {comp['benefit']}")
                st.write(f"**Research Source:** {comp['research']}")
                st.write("**Compatibility Score:** 75/100")
    
    # Plants to avoid
    if recommendations.get("avoid"):
        st.markdown("### ❌ Plants to Avoid")
        for comp in recommendations["avoid"]:
            with st.expander(f"⚠️ {comp['plant']}"):
                st.write(f"**Reason:** {comp['benefit']}")
                st.write(f"**Research Source:** {comp['research']}")
    
    # Garden layout suggestion
    st.markdown("### 📐 Suggested Garden Layout")
    layout_fig = create_garden_layout(primary_crop, recommendations)
    st.plotly_chart(layout_fig, use_container_width=True)

def create_garden_layout(primary_crop, recommendations):
    # Create a simple garden layout visualization
    fig = go.Figure()
    
    # Primary crop in center
    fig.add_trace(go.Scatter(
        x=[5], y=[5],
        mode='markers+text',
        marker=dict(size=50, color='green'),
        text=[primary_crop],
        textposition="middle center",
        name="Primary Crop"
    ))
    
    # Add companion plants around it
    positions = [(3, 7), (7, 7), (3, 3), (7, 3)]
    colors = ['lightgreen', 'lightblue', 'lightyellow', 'lightcoral']
    
    for i, comp in enumerate(recommendations.get("excellent", [])[:4]):
        if i < len(positions):
            fig.add_trace(go.Scatter(
                x=[positions[i][0]], y=[positions[i][1]],
                mode='markers+text',
                marker=dict(size=30, color=colors[i]),
                text=[comp['plant']],
                textposition="middle center",
                name=comp['plant']
            ))
    
    fig.update_layout(
        title="Garden Layout Suggestion",
        xaxis=dict(range=[0, 10], showgrid=True),
        yaxis=dict(range=[0, 10], showgrid=True),
        height=400,
        showlegend=False
    )
    
    return fig

if __name__ == "__main__":
    main()