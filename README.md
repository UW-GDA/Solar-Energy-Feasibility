# Spokane County Solar Suitability – Areeba Usman & Rose Martin  

![NASA Power Globe](Data/power_globe.gif)

## Introduction  
This project aims to identify lands that are well suited for 100 to 200 acre solar farms within Spokane County. The criteria used in the selection process included:
    - Flood plain data
    - Average solar radiation, from NASA POWER ARD, which takes into account average cloud cover. 
    - Land Use Zoning
    - Distance from the nearsest substation
    

To determine the areas with the highest solar farm potential, we assessed the four factors from above, creating a weighted score raster that combined the different variables into a single number for each pixel. An area of 150 acres was used as the ideal farm size. All the location at which such a farm was possible was identified along with the cumulative solar score was calcualted for each location. The high scoring attributes included areas with:
- High solar radiation.  
- Slope of 5 degrees or lower
- Within 5km of a substation
- Not within a floodplain

---

## Datasets  
We will use the following datasets for our analysis:  

- **NASA - Prediction of Worldwide Energy Resources (POWER ARD)**  
  - Variable: **All Sky Surface Shortwave Downward Direct Irradiance (DIR)**.  
- **NOAA - Local Climatological Data** (`LCD_USW00024157_2024.csv`)  
- **USGS - DEM Data**  
- **Home Facts - UV Map**  
- **Lidar - Washington Elevation Map**
  
---

## Problem Statement / Objectives  
To identify areas within Spokane suitable for a shared, residential solar farm, we will consider the following factors:  

### **Solar Irradiance**  
- Ideal locations receive **4–6 peak sun hours per day**.  
- High **Direct Normal Irradiance (DNI)** is preferred for solar farms.
- Our data computes a binary raster, showing the average total solar exposure over the course of the most recent year - 2024. This will explain why the range of radiatiom is from 0.48 to 0.498.  

### **Geographic Features**  
- Typically, lower elevation sites with stable weather conditions are preferred.  
- High-altitude locations can be viable but may face snow coverage issues.  

### **Tree Cover & Shading**  
- Minimal tree cover ensures optimal sunlight exposure.  
- Land clearing may be necessary, but environmental impact assessments should be conducted.  

### **Minimum Land Requirements**  
- **Minimum 150 acres of land**
- The land must not be in a flood zone, maintain close proximity to a substation,   

### **Proximity to Infrastructure**  
- Close to **existing power lines and substations** to reduce transmission losses and costs.  
- **Road access** for maintenance and construction.  

### **Key Research Questions**  
1. How does elevation affect solar radiation?  
2. How do these factors combine to create an ideal environment for solar energy?  
3. What socio-economic factors impact solar adoption in high-potential areas?  

---

 

---
## Tools and Software
- Geopandas
- xarray
- matplotlib
- seaborn
- censusdata
- contextily
---

## Map Making Methods  
- Use **geopandas** to filter flat land and remove national parks.  
- Use **if/else conditional statements** to categorize potential into **Low, Medium, and High**.  

---

## Planned Methodology  
1. **Identify Spokane County Boundaries**  
   - Isolate multipolygon for Spokane County.  
2. **Create a UV Radiation Map**  
   - Identify locations with high radiation levels.  
3. **Analyze Vegetation Impact**  
   - Generate an **NDVI raster** to classify vegetation levels.  
   - Convert raster to a DataFrame and categorize vegetation from **1 to 6**.  
   - Overlay vegetation data with radiation potential on a heatmap.  
4. **Determine Feasibility**  
   - Select the **top three** locations with the highest solar potential.  
   - Analyze feasibility based on:  
     - **Income levels**  
     - **Energy costs**  
     - **Tax incentives for solar**  
     - **Community attitudes towards solar adoption**  
   - Gather statistics and policies from reputable online sources (avoiding Census data).  

---

## Goals  

### **Main Goals**  
- **Map Variable Inputes solar radiation predictions**, considering cloud cover and elevation.  
- **Classify areas as High, Medium, or Low potential** for feasibility analysis.  
- **Predict feasibility** in high-potential areas based on socio-economic factors.  

### **Lower Priority Goal**  
- Identify **large exposed land** close to towns for potential solar farm development.  

---

## Expected Outcomes 
- A final map of Spokane County with the top three locations for solar stared.
- A zoomed-in map of all three locations with the calculated characteristics (predicted energy generation, land cost, etc.) for each parcel of land.


---

## References  
- [Land Requirements for Solar Farms](https://mysunshare.com/blog/land-requirement-for-solar-farm/#:~:text=solar%20farm%20development.-,Land%20size,revenue%20in%20the%20long%20run.)  
- [Considerations for Building a Solar Farm](https://greendealflow.com/considerations-when-building-a-solar-farm#:~:text=The%20first%20consideration%20is%20the,of%20peak%20sun%20per%20day.)  
