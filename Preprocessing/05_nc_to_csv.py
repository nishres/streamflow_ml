
import xarray as xr
import os
#import glob
#import re

cwd = os.path.abspath(os.getcwd())
# Input section to be defined by the user

print(cwd)
all_basins = os.listdir()


daily_mean = ['u10', 'v10' ,'t2m' ,'d2m' ,'skt' ,'stl1' ,'swvl1' ,
              'swvl2' ,'swvl3' ,'swvl4','src','sde' ,'snowc']
daily_total = ['tp' ,'ro' ,'sro' ,'ssro','e','sf', 'slhf']
daily_min = ['t2m','skt' ]
daily_max = ['t2m','skt' ]



for basin in all_basins:
    in_folder_path = cwd +'/'+ basin + '/' + '01_Daily' + '/' +'02_Merged_by_var'
    out_folder_path = cwd +'/'+ basin + '/' + '01_Daily' + '/' +'03_Csv'
    if not os.path.isdir(out_folder_path):
        os.makedirs(out_folder_path)
       
    for file in os.listdir(in_folder_path):
        filepath = os.path.join(in_folder_path,file)
        ds = xr.open_dataset(filepath)
        variables_list = list(ds.keys())
        if 'mean' in file:
            for var in variables_list:
                if var in daily_mean:
                    out_file = os.path.join(out_folder_path , f'{var}_mean.csv')
                    ds[var].to_dataframe().to_csv(out_file)
        elif 'min' in file:
            for var in variables_list:
                if var in daily_min:
                    out_file = os.path.join(out_folder_path , f'{var}_min.csv')
                    ds[var].to_dataframe().to_csv(out_file)
        elif 'max' in file:
            for var in variables_list:
                if var in daily_max:
                    out_file = os.path.join(out_folder_path , f'{var}_max.csv')
                    ds[var].to_dataframe().to_csv(out_file)
                elif var in daily_total:
                    out_file = os.path.join(out_folder_path , f'{var}_sum.csv')
                    ds[var].to_dataframe().to_csv(out_file)
        
    print(f'{basin} complete')
