
import xarray as xr
import os

#Extract basin extents
import geopandas as gpd
import pandas as pd
gdf = gpd.read_file("D:/Study_Area/thiessen_basins2/All_basins.shp")

#print(gdf.geometry.bounds)

df = pd.concat([gdf[['River','Location']],gdf.bounds],axis = 1)
#df['Station_ID'] = df['Station_ID'].astype(str)
df = df.round(2)

df['minx'] = df['minx'] - 0.1
df['miny'] = df['miny'] - 0.1
df['maxx'] = df['maxx'] + 0.1
df['maxy'] = df['maxy'] + 0.1

print(df)
aa = input('Press:')
#Input Folder Location
folder_path = 'D:/ERA5/All_Nepal'
# Output_FolderLocation
output_folder = 'D:/ERA5/Basins'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

data_folders=["Meteorology","Subsurface_hydrology",
              "Surface_Hydrology1","Surface_Hydrology2"]



# Function to clip a NetCDF file based on latitude and longitude bounds
def clip_nc(file_path, output_path, lat_min, lat_max, lon_min, lon_max):
    ds = xr.open_dataset(file_path)    
    # Clip based on latitude and longitude bounds
    clipped_ds = ds.sel(latitude=slice(lat_max, lat_min), longitude=slice(lon_min, lon_max))
    
    # Save the clipped data to a new NetCDF file
    clipped_ds.to_netcdf(output_path)
    
    ds.close()

for index,rows in df.iterrows():
    lat_min, lat_max = rows['miny'], rows['maxy'] 
    lon_min, lon_max = rows['minx'], rows['maxx']  
    for data_folder in data_folders:
        in_folder_path=os.path.join(folder_path,data_folder)
        basin_path = rows['River'] + '_' + rows['Location']+'/'+'00_Hourly' +'/'+data_folder
        data_output_folder=os.path.join(output_folder,basin_path) 
        if os.path.exists(data_output_folder):
            continue
        os.makedirs(data_output_folder)
        # Clip each file individually
        for filename in os.listdir(in_folder_path):
            if filename.endswith(".nc"):
                file_path = os.path.join(in_folder_path, filename)
                output_path = os.path.join(data_output_folder, f"{filename}")
                print(f'Çlipping {rows['River']},{rows['Location']} {filename}')
                clip_nc(file_path, output_path, lat_min, lat_max, lon_min, lon_max)
        #a = input(f'{rows['River']},{rows['Location']} complete. Press any key for next basin.')
print("Çomplete")

