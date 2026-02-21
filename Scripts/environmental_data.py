import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# --- CONFIGURATION ---
neighborhoods = [
    {"id": 1, "name": "Industrial Heights", "zone": "Industrial", "pop": 50000, "dist": 12},
    {"id": 2, "name": "Green Valley", "zone": "Residential", "pop": 35000, "dist": 15},
    {"id": 3, "name": "Downtown Core", "zone": "Commercial", "pop": 80000, "dist": 2},
    {"id": 4, "name": "East Port", "zone": "Industrial", "pop": 45000, "dist": 8},
    {"id": 5, "name": "Westside Suburbs", "zone": "Residential", "pop": 60000, "dist": 20},
    {"id": 6, "name": "Central Business District", "zone": "Commercial", "pop": 25000, "dist": 1},
    {"id": 7, "name": "North Park", "zone": "Residential", "pop": 40000, "dist": 10},
    {"id": 8, "name": "South Refinery", "zone": "Industrial", "pop": 30000, "dist": 14},
    {"id": 9, "name": "Riverside", "zone": "Residential", "pop": 55000, "dist": 5},
    {"id": 10, "name": "Market District", "zone": "Commercial", "pop": 42000, "dist": 4},
]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)
date_range = pd.date_range(start_date, end_date, freq='h')

# 1. GENERATE LOCATIONS CSV
df_locations = pd.DataFrame([
    {
        "location_id": n["id"],
        "neighborhood_name": n["name"],
        "zone_type": n["zone"],
        "population_density": n["pop"],
        "avg_income_level": random.randint(35000, 95000),
        "distance_from_city_center_km": n["dist"]
    } for n in neighborhoods
])

# 2. GENERATE WEATHER DATA CSV (Daily)
weather_records = []
daily_range = pd.date_range(start_date, end_date, freq='D')

for date in daily_range:
    for n in neighborhoods:
        # Simple seasonal logic: colder in Jan/Feb, warmer in June
        month = date.month
        base_temp = 10 if month < 3 else (25 if month > 5 else 18)
        
        is_rainy = random.random() < 0.2  # 20% chance of rain
        weather_records.append({
            "date": date.date(),
            "location_id": n["id"],
            "temperature": round(np.random.normal(base_temp, 5), 1),
            "humidity": random.randint(40, 90),
            "wind_speed": round(random.uniform(2, 25), 1),
            "rainfall": round(random.uniform(5, 20), 1) if is_rainy else 0.0
        })

df_weather = pd.DataFrame(weather_records)

# 3. GENERATE AIR QUALITY READINGS CSV (Hourly)
aqi_records = []
for date_time in date_range:
    for n in neighborhoods:
        # Logic: Industrial zones and closer to center = higher pollution
        base_aqi = 40
        if n["zone"] == "Industrial": base_aqi += 40
        if n["dist"] < 5: base_aqi += 20
        
        # Rush hour spikes (8-9 AM and 6-7 PM)
        hour = date_time.hour
        if hour in [8, 9, 18, 19]:
            base_aqi += 50
        
        # Weather impact: Rain cleans the air
        day_weather = df_weather[(df_weather['date'] == date_time.date()) & 
                                 (df_weather['location_id'] == n['id'])].iloc[0]
        if day_weather['rainfall'] > 0:
            base_aqi -= 30
            
        # Add randomness and calculate components
        final_aqi = max(10, int(np.random.normal(base_aqi, 15)))
        
        # Determine Category
        category = "Good"
        if final_aqi > 50: category = "Moderate"
        if final_aqi > 100: category = "Unhealthy for Sensitive Groups"
        if final_aqi > 150: category = "Unhealthy"

        aqi_records.append({
            "reading_id": len(aqi_records) + 1,
            "date": date_time.date(),
            "hour": hour,
            "location_id": n["id"],
            "PM2.5": round(final_aqi * 0.6, 1),
            "PM10": round(final_aqi * 0.8, 1),
            "NO2": round(random.uniform(10, 50), 1),
            "CO": round(random.uniform(0.1, 2.0), 1),
            "O3": round(random.uniform(5, 40), 1),
            "AQI_value": final_aqi,
            "AQI_category": category
        })

df_aqi = pd.DataFrame(aqi_records)

# Introduce 2% missing values for cleaning practice
for col in ['PM2.5', 'AQI_value']:
    df_aqi.loc[df_aqi.sample(frac=0.02).index, col] = np.nan

# 4. GENERATE HEALTH INCIDENTS CSV
health_records = []
incident_types = ["asthma_attack", "respiratory_infection", "hospital_visit"]
age_groups = ["0-17", "18-64", "65+"]
severities = ["mild", "moderate", "severe"]

# Create incidents based on pollution (with 1-day lag)
for i in range(2500):
    # Pick a random date (not the first day to allow for lag logic)
    rand_date = start_date + timedelta(days=random.randint(1, 180))
    rand_loc = random.choice(neighborhoods)
    
    # Check AQI from previous day to influence probability
    prev_day = (rand_date - timedelta(days=1)).date()
    avg_aqi_prev = df_aqi[(df_aqi['date'] == prev_day) & 
                          (df_aqi['location_id'] == rand_loc['id'])]['AQI_value'].mean()
    
    # If AQI was high, we are more likely to generate an incident here
    chance = random.random()
    if avg_aqi_prev > 120 or chance > 0.7:
        health_records.append({
            "incident_id": i + 1,
            "date": rand_date.date(),
            "location_id": rand_loc['id'],
            "incident_type": random.choice(incident_types),
            "age_group": random.choice(age_groups),
            "severity": random.choice(severities)
        })

df_health = pd.DataFrame(health_records)

# --- EXPORT DATA ---
df_locations.to_csv("locations.csv", index=False)
df_weather.to_csv("weather_data.csv", index=False)
df_aqi.to_csv("air_quality_readings.csv", index=False)
df_health.to_csv("health_incidents.csv", index=False)

print("Phase 1 Complete: All 4 CSV files generated successfully.")