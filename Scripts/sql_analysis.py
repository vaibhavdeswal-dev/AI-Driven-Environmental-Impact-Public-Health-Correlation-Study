import pandas as pd
import sqlite3
import os

# These 'print' lines are what you will see in your terminal
print("--- 1. Starting SQL Analysis Script ---")

# 1. CONNECT TO THE DATABASE
# This creates the actual 'city_health_analysis.db' file
connection = sqlite3.connect("city_health_analysis.db")
print("--- 2. Database connected successfully ---")

# 2. UPLOAD DATA
try:
    print("--- 3. Uploading CSVs to SQL tables... ---")
    
    # 1. Master data is inside 'my_final_files'
    pd.read_csv("my_final_files/master_combined_data.csv").to_sql("air_quality", connection, if_exists="replace", index=False)
    
    # 2. Locations is in the main folder
    pd.read_csv("locations.csv").to_sql("locations", connection, if_exists="replace", index=False)
    
    # 3. Weather is in the main folder
    pd.read_csv("weather_data.csv").to_sql("weather", connection, if_exists="replace", index=False)
    
    # 4. Health is named 'health_incidents.csv' in the main folder (Fixed name)
    pd.read_csv("health_incidents.csv").to_sql("health", connection, if_exists="replace", index=False)
    
    print("--- 4. Data upload complete (All tables synced) ---")
except Exception as e:
    print(f"!!! Error uploading data: {e}")
    
    
# 3. RUN A TEST QUERY (The Analysis)
# This asks the database to calculate the average pollution per neighborhood
print("--- 5. Running SQL Query: Average AQI per Neighborhood ---")

query = """
SELECT neighborhood_name, AVG(AQI_value) as average_pollution
FROM air_quality
GROUP BY neighborhood_name
ORDER BY average_pollution DESC;
"""

try:
    df_results = pd.read_sql(query, connection)
    print("\n--- YOUR SQL RESULTS TABLE ---")
    print(df_results)
    print("------------------------------\n")
except Exception as e:
    print(f"!!! Error running query: {e}")

# 4. CLOSE CONNECTION
connection.close()
print("--- 6. Script finished successfully ---")

# ==========================================================
# FINAL STEP: DATA ENGINEERING FOR POWER BI
# ==========================================================
import sqlite3
import pandas as pd

print("\n--- 7. Starting Final Data Engineering for Power BI ---")

# Connect to the database we built earlier
connection = sqlite3.connect("city_health_analysis.db")

# This is the "Analytical Query"
# It joins Air Quality, Locations, and Weather into one table
# and uses a subquery to count health incidents for each hour/area.
analytical_query = """
SELECT 
    a.date,
    a.hour,
    a.neighborhood_name,
    l.zone_type,
    l.population_density,
    a.AQI_value,
    w.temperature,
    w.wind_speed,
    w.rainfall,
    (SELECT COUNT(*) FROM health h 
     WHERE h.date = a.date 
     AND h.location_id = a.location_id) as incident_count
FROM air_quality a
LEFT JOIN locations l ON a.location_id = l.location_id
LEFT JOIN weather w ON a.date = w.date AND a.location_id = w.location_id;
"""



try:
    # 1. Run the query and load into a Dataframe
    df_powerbi = pd.read_sql(analytical_query, connection)

    # 2. Logic Check: Fill empty incident counts with 0 (so charts don't break)
    df_powerbi['incident_count'] = df_powerbi['incident_count'].fillna(0)

    # 3. Create a 'Severity' Column (Feature Engineering)
    # This turns numbers into categories like "Good" or "Hazardous"
    df_powerbi['pollution_severity'] = pd.cut(df_powerbi['AQI_value'], 
                                             bins=[0, 50, 100, 150, 500], 
                                             labels=['Good', 'Moderate', 'Unhealthy', 'Hazardous'])

    # 4. EXPORT THE FINAL FILE
    df_powerbi.to_csv("powerbi_final_data.csv", index=False)
    
    print("--- 8. SUCCESS: 'powerbi_final_data.csv' is generated! ---")
    print(f"Total records processed: {len(df_powerbi)}")
    print("This is your core project dataset ready for Power BI.")

except Exception as e:
    print(f"!!! Error during modeling: {e}")

finally:
    connection.close()