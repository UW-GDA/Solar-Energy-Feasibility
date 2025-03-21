# Spokane County Solar Suitability – Areeba Usman & Rose Martin  

![NASA Power Globe](Data/power_globe.gif)

## Introduction  
This project aims to identify lands that are well suited for 100 to 200-acre solar farms within Spokane County. The criteria used in the selection process included:
- Flood plain data
- Average solar radiation from NASA POWER ARD, accounting for average cloud cover
- Land Use Zoning
- Distance from the nearest substation

To determine the areas with the highest solar farm potential, we assessed the four factors above, creating a weighted score raster that combined the different variables into a single number for each pixel. An area of 150 acres was used as the ideal farm size. All locations where such a farm was possible were identified, and the cumulative solar score was calculated for each location. High-scoring attributes included areas with:
- High solar radiation  
- A slope of 5 degrees or lower  
- Within 5 km of a substation  
- Not within a floodplain  

---

## Datasets  
We used the following datasets for our analysis:  

- **NASA - Prediction of Worldwide Energy Resources (POWER ARD)**  
  - Variable: **All Sky Surface Shortwave Downward Direct Irradiance (DIR)**
  - Takes the total exposure for each given day and creates a percentage for each year per pixel.
- **ESA Land Cover Data**
  - Exported from **ArcGIS Pro** 
- **DEM WA COP90 Data** provided from class

---

## Problem Statement / Objectives  
To identify areas within Spokane suitable for a shared, residential solar farm, we considered the following factors:  

![Solar Irradiance](https://pub.mdpi-res.com/sustainability/sustainability-16-06436/article_deploy/html/images/sustainability-16-06436-g001.png?1722073377)

### **Solar Irradiance**  
- Ideal locations receive **4–6 peak sun hours per day**  
- High **Direct Normal Irradiance (DNI)** is preferred for solar farms  
- Our data computes a binary raster, showing the average total solar exposure over the most recent year (2024), with a range of **0.48 to 0.498**  

### **Geographic Features**  
- Lower elevation sites with stable weather conditions are preferred  
- High-altitude locations may face snow coverage issues  


![ESA Land Use](https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2008/12/envisat_global_land_cover_map/10265030-2-eng-GB/Envisat_global_land_cover_map_pillars.jpg)

### **Tree Cover & Shading - Land Use**  
- Minimal tree cover ensures optimal sunlight exposure  
- Land clearing may be necessary, but environmental impact assessments are advised  

### **Minimum Land Requirements**  
- **Minimum 150 acres of land**  
- The land must not be in a flood zone and must maintain close proximity to a substation  

### **Proximity to Infrastructure**  
- Close to **existing power lines and substations** to reduce transmission losses and costs  
- **Road access** for maintenance and construction  

### **Key Research Question**  
1. Where in Spokane County can we place a solar farm?

---

## Tools and Software
- Geopandas  
- Xdarray  
- Matplotlib  
- censusdata
- requests   

---

## Map Making Methods  
- Convert all data to raster and merge into an **xarray** dataframe  
- Classify each data variable by potential and remove classifications of land cover determined to be unusable for new infrastructure  
- Calculate net scores to determine filtration for possible locations  

---

## Planned Methodology  
1. **Identify Spokane County Boundaries**  
   - Isolate Tract Geometries for Spokane County
   - Create a equal area projection around county
   - Load in all data, clip and project to county.
2. **Merge to XdArray and Classify**  
   - Merge to dataframe, and create summary table to help identify ranges for classes/scales.
   - Create classes/scales, and set all values where a farm cannot be built to nan to remove places that will objectively cause disruption to the communities and environment.
3. **Computer Net Score to Determine Percentile Filter**  
   - Compute a weighted net score, ensuring slope and substation distance are weighed higher.
   - Use this to determine top highest scores and conclude top locations.
4. **Compute Total Solar Energy Produced per location**
   - This will aid in determining the top 3 locations
5. **Online Research: Compare energy policies and incentives per location (Or if close by, then tract), to decide which the overall best location.**
6. **Build the farm!**


---
![Farm](https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c29sYXIlMjBmYXJtfGVufDB8fDB8fHww)

## Goals  

### **Main Goals**  
- **Map solar radiation predictions** considering cloud cover and elevation  
- **Classify areas as High, Medium, or Low potential** for feasibility analysis
- Identify **large exposed land** close to towns for potential solar farm development 

### **Lower Priority Goal**  
- **Predict feasibility** in high-potential areas based on socio-economic factors  
  

---

## Expected Outcomes  
- A final map of Spokane County with the top three locations for solar farms  
- A zoomed-in map of all three locations with the calculated characteristics (predicted energy generation, land cost, etc.) for each parcel of land  

---

## References  
- [Land Requirements for Solar Farms](https://mysunshare.com/blog/land-requirement-for-solar-farm/#:~:text=solar%20farm%20development.-,Land%20size,revenue%20in%20the%20long%20run.)  
- [Considerations for Building a Solar Farm](https://greendealflow.com/considerations-when-building-a-solar-farm#:~:text=The%20first%20consideration%20is%20the,of%20peak%20sun%20per%20day.)  

