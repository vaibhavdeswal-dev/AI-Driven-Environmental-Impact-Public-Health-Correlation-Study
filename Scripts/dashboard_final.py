import pandas as pd
import plotly.express as px

print("Loading master data for visualization...")
df = pd.read_csv("my_final_files/master_combined_data.csv")

# This identifies the "Problem Areas" (The 'Why' of your project)
neighborhood_stats = df.groupby('neighborhood_name')['AQI_value'].mean().sort_values().reset_index()
fig1 = px.bar(neighborhood_stats, 
             x='AQI_value', 
             y='neighborhood_name', 
             orientation='h',
             title="Air Quality Ranking by Neighborhood (Lower is Cleaner)",
             color='AQI_value',
             color_continuous_scale='RdYlGn_r') # Red for high, Green for low

# This shows the "Rush Hour" effect you found in SQL
hourly_stats = df.groupby('hour')['AQI_value'].mean().reset_index()
fig2 = px.line(hourly_stats, 
              x='hour', 
              y='AQI_value', 
              title="Average Pollution Trend Throughout the Day",
              markers=True)

#  RESULTS
print("Opening dashboard in your browser...")
fig1.show()
fig2.show()