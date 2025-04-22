
#import xarray as xr
import os
import pandas as pd


#cwd = os.path.abspath(os.getcwd())
# Input section to be defined by the user

#print(cwd)
all_basins = os.listdir()
all_variables = ['u10', 'v10' ,'t2m' ,'d2m' ,'skt' ,'stl1' ,'swvl1' ,
              'swvl2' ,'swvl3' ,'swvl4','src','sde' ,'snowc',
              'tp' ,'ro' ,'sro' ,'ssro','e','sf', 'slhf']

daily_mean = ['u10', 'v10' ,'t2m' ,'d2m' ,'skt' ,'stl1' ,'swvl1' ,
              'swvl2' ,'swvl3' ,'swvl4','src','sde' ,'snowc']
daily_total = ['tp' ,'ro' ,'sro' ,'ssro','e','sf', 'slhf']
daily_min = ['t2m','skt' ]
daily_max = ['t2m','skt' ]


def get_thiessen_geometry(path_1):
    for file_1 in os.listdir(path_1):
        if file_1.endswith('.xlsx'):
            xls_path = os.path.join(path_1,file_1)
            break
    df = pd.read_excel(xls_path)
    df['Th_wt'] = df['Area_km2']/df['Area_km2'].sum()   
    df = df[(df['Th_wt'] > 0.001) | (df['Area_km2'] > 3)]
    df['Grid'] = df['Latitude'].astype(str) + 'N,' + df['Longitude'].astype(str) + 'E'
    df['Th_wt'] = df['Area_km2']/df['Area_km2'].sum()     
    df = df[['Grid', 'Th_wt']]
    out_path_1 = os.path.join(path_1,'thiessen_wt.csv')
    df.to_csv(out_path_1)
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df.iloc[1:,:]
    return df

            
def get_basin_era_data(path_2,grid_2,var_2):
    # print(path_2)
    # print(grid_2)
    print(var_2)    
    
    df = pd.read_csv(path_2)        
    df['Grid'] = df['latitude'].astype(str) + 'N,' + df['longitude'].astype(str) + 'E'   
    df = df[['time','Grid',var_2]]
    df = pd.pivot_table(df,index= 'time', columns= 'Grid', values= var_2)
    for cols in df.columns.to_list():
        if cols not in grid_2:
            #print(cols)
            df = df.drop(columns = cols,axis = 1)
    return df

def get_agg(file_3):
    if 'mean' in file_3:
        return 'mean'
    elif 'min' in file_3:
        return 'min'
    elif 'max' in file_3:
        return 'max'
    elif 'sum' in file_3:
        return 'sum'
    else:
        print('Error in file name')


all_covariates = []
for variable in all_variables:
    if variable in daily_mean:
        all_covariates.append(f'{variable}_mean')
    if variable in daily_min:
        all_covariates.append(f'{variable}_min')
    if variable in daily_max:
        all_covariates.append(f'{variable}_max')
    if variable in daily_total:
        all_covariates.append(f'{variable}_sum')            

#print(all_covariates)
count = 0
for basin in all_basins:
    if basin == 'Sabhyakhola_Tumlingtar':
        continue
    print(basin)
    # count += 1
    # if count < 28:
    #     continue
    #a = input('Press:')
    print(f'{basin}_start')
    d = {}
    for i in all_covariates:
        d[i] = pd.DataFrame()
    
    basin_path = 'D:/Study_Area/Sub_Basin/xls/Sub_Basin_mean'
    df_th_wt = get_thiessen_geometry(basin_path)
    df_th_wt = df_th_wt.sort_index(axis = 1)
    print(df_th_wt)
    all_gridpoints = df_th_wt.columns.to_list()
    
    in_folder_path = basin_path + '/' + '01_Daily' + '/' +'03_Csv'
    # out_folder_path = basin_path + '/' + 'Daily' + '/' +'04.Basin_Mean'
    # if not os.path.isdir(out_folder_path):
    #     os.makedirs(out_folder_path)
        
    for file in os.listdir(in_folder_path):
        if file.endswith('.csv'):
            for var in all_variables:
                if file.startswith(var):
                    break
            agg = get_agg(file)
            csv_path = os.path.join(in_folder_path,file)
            df_era = get_basin_era_data(csv_path,all_gridpoints,var)
        else:
            print('No csv file')
        
        df_era = df_era.sort_index(axis = 1)
        
        # print(df_th_wt)
        # print()
        # print(df_era)  
        
        #a = input('1Press:')

        for index,rows in df_era.iterrows():
            weighted = 0.0
            #print(index)
            for gridpoint in all_gridpoints:
                col_index = df_th_wt.columns.get_loc(gridpoint)
                #print(rows[gridpoint],df_th_wt.iloc[0,col_index])
                #a = input('1Press:')
                weighted += rows[gridpoint] * df_th_wt.iloc[0,col_index]
                #print(type(weighted))
            df_era.at[index,'Th_wt'] = weighted
        # print()
        # print(df_era)
        
        d[f'{var}_{agg}'] = df_era[['Th_wt']]
        d[f'{var}_{agg}'].rename(columns = {'Th_wt':f'{var}_{agg}'},inplace = True)
        #print(d[f'{var}_{agg}'])
        #a = input('2Press:')
    #print(d)
    df_basin_mean = pd.concat(d.values(),axis = 1,ignore_index= False)
    print(df_basin_mean)
    out_file = os.path.join(basin_path,f'{basin}_basin_avg.csv')
    df_basin_mean.to_csv(out_file)
    print(f'{basin}_complete')
    

                    
 
