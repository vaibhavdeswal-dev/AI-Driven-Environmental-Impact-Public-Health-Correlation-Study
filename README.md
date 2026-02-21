
## Project Overview

This project investigates the relationship between urban air quality, local weather patterns, and public health outcomes. By integrating disparate datasets—including air quality indices (AQI), weather metrics, and hospital incident logs—I developed a full-stack analytical suite that identifies the core environmental drivers behind health crises in urban areas.

---

## The Stack

- **Data Engineering:** Python (Pandas/NumPy) for ETL and data cleaning.
- **Database Management:** SQL (SQLite) for relational data modeling and querying.
- **Analytics & AI:** Power BI (DAX, AI Key Influencers, Decomposition Trees).
- **Visual Design:** Custom dark-themed UI focused on user experience (UX) and accessibility.

---

## Key Insights & Dashboards

### 1. Executive Overview

- **Dynamic Tracking:** Real-time monitoring of city-wide AQI (Avg: 60) and health incident totals (8,568).
- **Automated Risk Segmentation:** Used a Decomposition Tree to intelligently break down incident counts by zone type and pollution severity.
- **Prioritized Action:** Identified the "Top 5 High-Risk Neighborhoods" based on historical AQI trends to assist in resource allocation.
- <img width="1232" height="680" alt="image" src="https://github.com/user-attachments/assets/d59ce514-98c6-4175-8c9b-6f23e1243bb3" />




### 2. Root Cause Discovery (AI-Driven)

- **Environmental Correlation:** Proven statistical link between wind speed and air quality—higher average wind speeds significantly correlate with lower AQI values.
- **AI Influencer Analysis:** Leveraged Machine Learning to determine that specific temperature ranges (27.7°C - 28.3°C) and rainfall patterns are primary drivers for health incident fluctuations.
- **Dynamic Ranking:** A Ribbon Chart tracks how neighborhoods swap pollution rankings month-to-month, highlighting seasonal environmental shifts.

- <img width="1221" height="682" alt="image" src="https://github.com/user-attachments/assets/31d225e5-e430-4d54-9a95-f5ae00daf6cb" />


---

## How It Was Built (From Scratch)

1. **Pipeline Construction:** Wrote `air_quality_analysis.py` to ingest and clean 3+ raw CSV datasets.
2. **Relational Modeling:** Developed `sql_analysis.py` to create a master database (`city_health_analysis.db`), ensuring data integrity and query efficiency.
3. **Visualization:** Designed a two-page interactive dashboard with seamless page navigation and high-contrast accessibility.
