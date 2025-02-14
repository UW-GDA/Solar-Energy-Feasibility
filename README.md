# Spokane County Solar Suitability – Areeba Usman & Rose Martin  

![NASA Power Globe](power_globe.gif)

## Introduction  
This project aims to predict and classify solar potential as well as determine feasibility in Spokane. We will start by identifying flat areas of land that are at least 10 acres and are close to towns, making them easier to develop and maintain as solar farms.  

To determine solar potential, we will consider cloud cover and elevation. Feasibility will be assessed based on income, energy costs, and incentives available for solar adoption. Using this data, we will:  
- Predict areas with high solar radiation.  
- Classify them as **High, Medium, or Low** potential.  
- Predict the likelihood of solar adoption for high-potential areas.  

---

## Problem Statement / Objectives  
To identify areas within Spokane suitable for a shared, residential solar farm, we will consider the following factors:  

### **Solar Irradiance**  
- Ideal locations receive **4–6 peak sun hours per day**.  
- High **Direct Normal Irradiance (DNI)** is preferred for solar farms.  

### **Geographic Features**  
- Typically, lower elevation sites with stable weather conditions are preferred.  
- High-altitude locations can be viable but may face snow coverage issues.  

### **Tree Cover & Shading**  
- Minimal tree cover ensures optimal sunlight exposure.  
- Land clearing may be necessary, but environmental impact assessments should be conducted.  

### **Minimum Land Requirements**  
- **Community-scale solar farm**: ~5–10 acres per MW.  
- **Utility-scale solar farm**: 50+ acres for multiple MW capacity.  

### **Proximity to Infrastructure**  
- Close to **existing power lines and substations** to reduce transmission losses and costs.  
- **Road access** for maintenance and construction.  

### **Key Research Questions**  
1. How does elevation affect solar radiation?  
2. How do these factors combine to create an ideal environment for solar energy?  
3. What socio-economic factors impact solar adoption in high-potential areas?  

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
- **Map solar radiation predictions**, considering cloud cover and elevation.  
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
