# -*- coding: utf-8 -*-
"""
Created on Dec  7 14:36:07 2024

@author: sthni
"""
import xarray as xr
import os
import glob

cwd = os.path.abspath(os.getcwd())
# Input section to be defined by the user

all_basins = os.listdir()

data_folders=["Meteorology","Subsurface_hydrology",
              "Surface_Hydrology1","Surface_Hydrology2"]

aggregate_type = ["Mean","Max","Min"]


for basin in all_basins:
    out_folder_path = cwd +'/'+ basin + '/' + '01_Daily' + '/' +'01_Merged_by_time'
    for agg in aggregate_type:
        for data_folder in data_folders:
            #in_folder_path = cwd + '/' + basin +'/' + 'Daily' + '/' + agg + '/' + data_folder
            in_folder_path = 'C:/Users/sthni/Desktop/Basins' + '/' + basin +'/' + '01_Daily' + '/00_' + agg + '/' + data_folder
            print(in_folder_path)
            
            #a = input('Press any key:')

            # List of clipped files
            ds_list = [xr.open_dataset(file) for file in glob.glob(f'{in_folder_path}/*.nc')]

            # Merge the clipped files into a single file
            ds_merged = xr.merge(ds_list)
            
            
            #print(out_folder_path)
            if not os.path.isdir(out_folder_path):
                os.makedirs(out_folder_path)
            out_file = os.path.join(out_folder_path , f'{basin}_{agg}_{data_folder}.nc')   
            ds_merged.to_netcdf(out_file)
