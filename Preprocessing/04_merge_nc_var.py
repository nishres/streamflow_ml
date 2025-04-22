# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:28:01 2024

@author: sthni
"""

import xarray as xr
import os


cwd = os.path.abspath(os.getcwd())
# Input section to be defined by the user


all_basins = os.listdir()



for basin in all_basins:
    in_folder_path = cwd +'/'+ basin + '/' + '01_Daily' + '/' +'01_Merged_by_time'
    out_folder_path = cwd +'/'+ basin + '/' + '01_Daily' + '/' +'02_Merged_by_var'
    
    if not os.path.isdir(out_folder_path):
        os.makedirs(out_folder_path)
        
    files_mean = [] 
    files_max = [] 
    files_min = [] 

    
    for file in os.listdir(in_folder_path):
        if 'Mean' in file:
            filepath = os.path.join(in_folder_path,file)
            files_mean.append(filepath)
        elif 'Max' in file:
            filepath = os.path.join(in_folder_path,file)
            files_max.append(filepath)
        elif 'Min' in file:
            filepath = os.path.join(in_folder_path,file)
            files_min.append(filepath)
    
    # print(files_mean)
    # print()
    # print(files_min)
    # print()
    # print(files_max)

    # a = input('Press:')       
    ds_mean = xr.merge([xr.open_dataset(f) for f in files_mean])
    out_file = os.path.join(out_folder_path,f'{basin}_mean.nc')
    ds_mean.to_netcdf(out_file)
    
    ds_min = xr.merge([xr.open_dataset(f) for f in files_min])
    out_file = os.path.join(out_folder_path,f'{basin}_min.nc')
    ds_min.to_netcdf(out_file)
    
    ds_max = xr.merge([xr.open_dataset(f) for f in files_max])
    out_file = os.path.join(out_folder_path,f'{basin}_max.nc')
    ds_max.to_netcdf(out_file)
    
    print(f'{basin} complete')
    
    # a = input('Press:') 
