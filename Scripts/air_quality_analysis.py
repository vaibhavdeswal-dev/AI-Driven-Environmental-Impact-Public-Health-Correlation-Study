import pandas as pd
import os

# --- STEP 1: BRING IN THE FILES ---
# We are just telling Python to go find those CSVs we made earlier
air_data = pd.read_csv("air_quality_readings.csv")
place_info = pd.read_csv("locations.csv")
weather_info = pd.read_csv("weather_data.csv")
health_info = pd.read_csv("health_incidents.csv")

print("Step 1: I've successfully grabbed all the raw files!")

# --- STEP 2: FIXING THE MISSING SPOTS ---
# Remember how we left some empty holes in the data? 
# We are telling Python: "If a number is missing, look at the neighbors and guess the middle value"
air_data['AQI_value'] = air_data['AQI_value'].interpolate()
air_data['PM2.5'] = air_data['PM2.5'].interpolate()

print("Step 2: Holes are filled! No more missing data.")

# --- STEP 3: MAKING THE DATA TALK TO EACH OTHER ---
# Right now, 'air_data' only has IDs. We want to see the actual Neighborhood Names.
# It's like matching a key to a lock using 'location_id'
combined_data = pd.merge(air_data, place_info, on="location_id")

# Now let's add the weather (Rain and Temp) into that same list
big_table = pd.merge(combined_data, weather_info, on=["date", "location_id"])

print("Step 3: All the files are now joined into one big master list.")

# --- STEP 4: SHRINKING THE DATA FOR THE DASHBOARD ---
# We have 40,000 rows (hourly). That's too much. 
# Let's just get the AVERAGE for each Day so it's easier to read.
daily_report = big_table.groupby(['date', 'neighborhood_name', 'zone_type']).agg({
    'AQI_value': 'mean',
    'temperature': 'mean',
    'rainfall': 'sum'
}).reset_index()

print("Step 4: I've shrunk the data into a nice daily summary.")


# We want to put these into a new folder so we don't mess up our original raw files
if not os.path.exists('my_final_files'):
    os.makedirs('my_final_files')

daily_report.to_csv("my_final_files/daily_summary.csv", index=False)
big_table.to_csv("my_final_files/master_combined_data.csv", index=False)

print("Step 5: Done! Look in the 'my_final_files' folder for the clean data.")