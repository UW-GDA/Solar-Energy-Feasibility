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

def calculate_date_before(date_str, days_padding=1):
    date = pd.Timestamp(date_str)  # Convert string to pandas Timestamp
    date_before = date - pd.DateOffset(days=days_padding)
    return date_before.strftime("%Y-%m-%d")

def calculate_date_range(date_str, months_padding=3):
    date = pd.Timestamp(date_str)  # Convert string to pandas Timestamp
    start_date = date - pd.DateOffset(months=months_padding)
    end_date = date + pd.DateOffset(months=months_padding)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def step_function(t, a, b, t0, k=10):
    return a + b / (1 + np.exp(-k * (t - t0))) 

def fit_step_function(observed_values, time_values, date_of_interest):
    """Fit step function to a single pixel time series."""
    # mask nodata values 
    mask = ~np.isnan(observed_values)
    
    if np.sum(mask) < 5:  # skip if not enough valid points
        return np.nan, np.nan, np.nan
    
    try:
        # convert valid values
        t_valid = time_values[mask].astype(float)
        observed_valid = observed_values[mask]

        # initial guesses: baseline observed value, rough estimate observed value change, and date of interest
        p0 = [0, -0.2, np.datetime64(date_of_interest).astype("datetime64[ns]").astype(float)]
        
        # fit the step function
        params, _ = curve_fit(step_function, t_valid, observed_valid, p0=p0)

        return params[0], params[1], params[2]  # a (baseline), b (step size), t0 (change date)

    except RuntimeError:
        return np.nan, np.nan, np.nan  # return NaN if fitting fails

