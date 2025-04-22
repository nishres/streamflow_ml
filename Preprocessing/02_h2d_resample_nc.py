# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 20:02:46 2024

@author: sthni
"""

import xarray as xr
import os


all_basins = os.listdir()

data_folders=["Meteorology","Subsurface_hydrology",
              "Surface_Hydrology1","Surface_Hydrology2"]
for basin in all_basins:
    print(basin)
    if basin != 'Sabhyakhola_Tumlingtar':
        for folder in data_folders:       
            r_source_path = basin + "/" + "00_Hourly" + "/" + folder
            abs_source_path = os.path.join(os.path.abspath(os.getcwd()),r_source_path)
            
            temp = 'C:/Users/sthni/Desktop/Basins'
            r_dest_path_mean = os.path.join(temp,basin) + '/' + "01_Daily" +'/' + '00_Mean' + '/' + folder
            r_dest_path_max = os.path.join(temp,basin) + '/' + "01_Daily" +'/' + '00_Max' + '/' + folder
            r_dest_path_min = os.path.join(temp,basin) + '/' + "01_Daily" +'/' + '00_Min' + '/' + folder        
            
            #r_dest_path_mean = os.path.join(os.path.abspath(os.getcwd()),basin) + '/' + "01_Daily" +'/' + '00_Mean' + '/' + folder
            #r_dest_path_total = os.path.join(os.path.abspath(os.getcwd()),basin) + '/' + "01_Daily" +'/' + '00_Sum' + '/' + folder
            if not os.path.exists(r_dest_path_mean):
                os.makedirs(r_dest_path_mean)
            if not os.path.exists(r_dest_path_max):
                os.makedirs(r_dest_path_max)
            if not os.path.exists(r_dest_path_min):
                os.makedirs(r_dest_path_min)
            for file in os.listdir(abs_source_path):
                if file.endswith(".nc"):
                    print(f'{basin} {folder} {file}')
                    file_source_path = os.path.join(abs_source_path, file)
                    
                    ds_hourly = xr.open_dataset(file_source_path)                    
                    ds_daily_mean = ds_hourly.resample(time='D').mean()
                    file_dest_path = os.path.join(r_dest_path_mean,file)
                    ds_daily_mean.to_netcdf(file_dest_path)
                    
                    ds_hourly = xr.open_dataset(file_source_path)
                    ds_daily_max = ds_hourly.resample(time='D').max()
                    file_dest_path = os.path.join(r_dest_path_max,file)
                    ds_daily_max.to_netcdf(file_dest_path)
                    
                    ds_hourly = xr.open_dataset(file_source_path)
                    ds_daily_min = ds_hourly.resample(time='D').min()
                    file_dest_path = os.path.join(r_dest_path_min,file)
                    ds_daily_min.to_netcdf(file_dest_path)

print('end')
