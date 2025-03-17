#!/usr/bin/env python

import utils
import pystac_client
import planetary_computer
import xarray as xr
import rasterio as rio
import rioxarray
import geopandas as gpd
import odc.stac
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import os
import rasterstats
from rioxarray import merge
import scipy.ndimage as ndimage
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.measure import label
from shapely.geometry import shape
from rasterio.features import shapes, rasterize
import xyzservices.providers as xyz
import argparse
from typing import Tuple

#Gets the NDVI from sentienel-2 pre earthquake, and uses the Red, NIR, and SCL bands to calculate NDVI
#Returns tehe seasonal averages of the calculated NDVIs
def get_seasonal_ndvi(earthquake_date, bbox, cloud_cover=80):

    #gets the starting and ending dates
    end_date = utils.calculate_date_before(earthquake_date)
    start_date = '2015-06-27'

    #Runs through the catalog and saves the data in items
    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
    search = catalog.search(collections = ["sentinel-2-l2a"], query={"eo:cloud_cover": {"lt": cloud_cover}}, bbox = bbox, datetime=(start_date, end_date))
    items = search.item_collection()

    #Saves the red, NIR, and SCL bands adn uses them to calculate NDVI
    pre_earthquake_s2_ds = odc.stac.load(items, bands=["B04","B08","SCL"], resolution=10,chunks={"x": 256, "y": 256},groupby='solar_day',bbox=bbox)
    pre_earthquake_s2_ds['NDVI'] = (pre_earthquake_s2_ds['B08'] - pre_earthquake_s2_ds['B04'])/(pre_earthquake_s2_ds['B08'] + pre_earthquake_s2_ds['B04'])

    # mask unreliable pixels
    bad_scl = [0, 1, 8, 9]
    pre_earthquake_s2_ds['NDVI'] = pre_earthquake_s2_ds['NDVI'].where(~pre_earthquake_s2_ds['SCL'].isin(bad_scl))
    
    # drop unnneeded data variables 
    pre_earthquake_s2_ds = pre_earthquake_s2_ds.drop_vars(['B04', 'B08', 'SCL'])

    #Groups by season
    season_ds = pre_earthquake_s2_ds.groupby("time.season").median("time").compute()
    return season_ds




#Gets a timesereis of one month before and after the earthquake of the NDVIs
#Also calculates the anomalies notes based off seasonal data
def get_ndvi_timeseries(earthquake_date, bbox, seasonal_ds, cloud_cover = 50, resoltuion=10):

    #gets the ranges of dates, around a month before and after the date of the earth quake
    date_range = utils.calculate_date_range(earthquake_date)
    
    #get the desired items form teh catalog and save them 
    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
    search = catalog.search(collections = ["sentinel-2-l2a"], query={"eo:cloud_cover": {"lt": cloud_cover}}, bbox = bbox, datetime=date_range)
    items = search.item_collection()

    #groups the band in by their solar day 
    s2_ds = odc.stac.load(items, bands=["B04","B08","SCL"], resolution=resoltuion, groupby='solar_day',chunks={"x": 256, "y": 256}, bbox = bbox)

    #creates the NDVI band
    s2_ds['NDVI'] = (s2_ds['B08'] - s2_ds['B04'])/(s2_ds['B08'] + s2_ds['B04'])
    
    # mask unreliable pixels
    cloud_nodata_values = [0, 1, 8, 9]
    s2_ds['NDVI'] = s2_ds['NDVI'].where(~s2_ds['SCL'].isin(cloud_nodata_values))
    
    # drop unnneeded data variables 
    s2_ds = s2_ds.drop_vars(['B04', 'B08', 'SCL'])

    # extract month index from the time dimension of the time series dataset
    s2_ds = s2_ds.assign_coords(season=s2_ds['time'].dt.season)
    
    # calcualate the ndvi anomaly by subtracting the median monthly NDVI for the appropriate month
    s2_ds['NDVI_anomaly'] = s2_ds['NDVI'] - seasonal_ds.sel(season=s2_ds['season'])['NDVI']
    
    s2_ds = s2_ds.compute()
    
    return s2_ds


# Creates landslide mask
def create_landslide_mask(earthquake_date, s2_ds):

    # calculate median pre-earthquake NDVI anomaly
    pre_earthquake_anomaly_da = s2_ds.where(s2_ds.time < pd.Timestamp(earthquake_date)).NDVI_anomaly.median(dim='time')

    # calculate median pre-earthquake NDVI anomaly
    post_earthquake_anomaly_da = s2_ds.where(s2_ds.time > pd.Timestamp(earthquake_date)).NDVI_anomaly.median(dim='time')
    
    # calculate the difference in median NDVI
    ndvi_anomaly_difference = post_earthquake_anomaly_da - pre_earthquake_anomaly_da

    # convert time to numeric for fitting
    time_numeric = s2_ds.time.values.astype(float)
    
    # apply the function!
    results = xr.apply_ufunc(
        utils.fit_step_function, 
        s2_ds.NDVI_anomaly,  # NDVI values
        time_numeric,  # time values (passed separately)
        earthquake_date, # intial guess for step date
        input_core_dims=[["time"], ["time"], []],  # apply function along time axis
        output_core_dims=[[], [], []],  # three scalar outputs per pixel
        vectorize=True,  # allows working on multiple pixels at once
        dask="parallelized",  # uses Dask
        output_dtypes=[float, float, float],  # data types of outputs
    )

    # add the NDVI anomaly step size as new data variable in our time series dataset
    s2_ds = s2_ds.assign(NDVI_anomaly_step=(["y", "x"], results[1].values))

    #create the NDVI anomaly mask
    values = (s2_ds.NDVI_anomaly_step <= -0.1).astype(int)
    #Save the dataset name as ""
    values.name = "landslide_mask"
    #Add the mask to the s2_ds data array
    
    s2_ds= xr.merge([s2_ds,values],compat='override')
    #s2_ds = s2_ds.assign(landslide_mask=(["y", "x"], values))

    return s2_ds



#Splits and identifies the individaul landslides
def segment_landslides(s2_ds):
    # define structuring element (3x3 cross or square)
    structure = np.ones((3, 3), dtype=bool) 
    
    # convert to NumPy array for processing
    mask_np = s2_ds['landslide_mask'].values
    
    # apply erosion followed by dilation (opening operation)
    eroded = ndimage.binary_erosion(mask_np, structure=structure)
    cleaned_mask = ndimage.binary_dilation(eroded, structure=structure)
    
    # assign the cleaned mask back to the dataset
    s2_ds = s2_ds.assign(landslide_mask_cleaned=(["y", "x"], cleaned_mask))

    # convert landslide mask to integer (1 = landslide, 0 = background)
    landslide_mask = s2_ds.landslide_mask_cleaned.values.astype(int)
    
    # compute distance from non-landslide pixel
    distance = ndimage.distance_transform_edt(landslide_mask)
    
    # get local maxima as coordinates
    coordinates = peak_local_max(distance, labels=landslide_mask, min_distance=5)
    
    # create an empty mask with the same shape as `distance`
    local_maxi = np.zeros_like(distance, dtype=bool)
    
    # set local maxima positions to True
    local_maxi[tuple(coordinates.T)] = True  # Convert coordinates to indices
    
    # give each local maxima a unique marker value
    markers, _ = ndimage.label(local_maxi)
    
    # apply watershed segmentation to separate landslides
    labeled_landslides = watershed(-distance, markers, mask=landslide_mask)
    
    # assign the split landslide IDs back to dataset
    s2_ds = s2_ds.assign(landslide_id=(["y", "x"], labeled_landslides))

    return s2_ds



#Creates a geojason file with the landslide instance and it's geometry
def polygonize_landslides(earthquake_date, bbox, s2_ds):
    # initialize list for polygons and values
    polygons = []
    values = []
    
    
    for geom, value in shapes(s2_ds.landslide_id.values, mask=s2_ds.landslide_id.values > 0, transform=s2_ds.rio.transform()):
        polygons.append(shape(geom))  # convert to Shapely polygon
        values.append(value)  # store landslide label

    
    # create GeoDataFrame
    landslides_gdf = gpd.GeoDataFrame({"landslide_id": values, "geometry": polygons}, crs=s2_ds.rio.crs)

    #name itinearry properly
    minx, miny, maxx, maxy = bbox
    landSlides_fn = f'landslides_{earthquake_date}_{minx}_{miny}_{maxx}_{maxy}.geojson'
    
    landslides_gdf.to_file(landSlides_fn, driver='GeoJSON')
    
    return None
    





def main():
        
    """
        minx: Minimum longitude of the bbox
        miny: Minumum latitude of the bbox
        maxx: Maximum longitude of the bbox
        maxy: Maximum latitude of the bbox
        earthquake_date
        cloud_cover_seasonal: maximum cloud cover for seasonal median NDVI
        cloud_cover_time_series: maximum cloud cover for NDVI time series
    """

    parser = argparse.ArgumentParser(description="Locates Potential Landslides after earthquakes using sentinel-2 data")

    parser.add_argument("minx", type=float, help="Minimum longitude of the bbox")
    parser.add_argument("miny", type=float, help="Minimum latitude of the bbox")
    parser.add_argument("maxx", type=float, help="Maximum longitude of the bbox")
    parser.add_argument("maxy", type=float, help="Maximum latitude of the bboxx")
    parser.add_argument("earthquake_date", type=str, help="Date of earthquake")
    parser.add_argument("cloud_cover_seasonal", type=int, help="maximum cloud cover for seasonal median NDVI")
    parser.add_argument("cloud_cover_time_series", type=int, help="maximum cloud cover for NDVI time series")

    args = parser.parse_args()
    
    earthquake_date = args.earthquake_date
    bbox = (args.minx, args.miny, args.maxx, args.maxy)
    cloud_cover_seasonal = args.cloud_cover_seasonal
    cloud_cover_time_series = args.cloud_cover_time_series

    print("Gets the seasonal ndvi of the given bbox from before the earthquake happened")
    seasonal_ds = get_seasonal_ndvi(earthquake_date, bbox, cloud_cover_seasonal)

    print("Returns a data array of the NDVI values a month before and after the earthquake")
    s2_ds = get_ndvi_timeseries(earthquake_date, bbox, seasonal_ds, cloud_cover_time_series)

    print("Creates a mask of the landslides")
    s2_ds = create_landslide_mask(earthquake_date, s2_ds)

    
    print("Splits and identifies the individaul landslides")
    s2_ds = segment_landslides(s2_ds)

    print("Creates a geojason file with the landslide instance and it's geometry")
    polygonize_landslides(earthquake_date, bbox, s2_ds)

    print("done")


if __name__ == "__main__":
    main()