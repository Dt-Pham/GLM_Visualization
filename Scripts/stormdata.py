import os
import pandas as pd
import numpy as np
import sys
import xarray as xr
from glmtools.io.glm import GLMDataset
import time

from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
from tqdm import tqdm

class DataReader:
    def __init__(self):
        self.data_folder = "./Data/"
        self.sample_glm_file = self.data_folder + "GLM/240/00/OR_GLM-L2-LCFA_G17_s20202400000000_e20202400000200_c20202400000225.nc"
        self.bbox = (-140, -30, 0, 60)

        # read csv file
        self.df = pd.read_csv(self.data_folder + "Laura/Hurricane_Laura_Trackfile_Spline.csv")
    
    def run(self):
        self.process_file(self.sample_glm_file, "test.png", edges=self.bbox)

    def process_file(self, datafile, output_file, edges=(-180,180,-90,90),buffer=0):
        data = GLMDataset(datafile).dataset
        
        # time data in format "YYYY-MM-DD HH:MM:SS"
        time_str = data.time_coverage_start[:-3].replace('T', ' ')
        
        row = self.df[self.df["Date"] == time_str]
        if row.empty: # if time is not in trackfile
            return
        
        # extract data about groups
        groups = data[['group_energy','group_area']]
        groups = groups.drop(['group_parent_flash_id','lightning_wavelength','product_time','group_time_threshold','flash_time_threshold','lat_field_of_view','lon_field_of_view'])
        
        # draw the figure
        fig = plt.figure(dpi=200)
        map = Basemap(projection='merc', llcrnrlon=edges[0]-buffer, llcrnrlat=edges[2]-buffer,  # lower-left longitude and lattitude
                    urcrnrlon=edges[1]+buffer,urcrnrlat=edges[3]+buffer,   # upper-right longitude and lattitude
                    lon_0=0,lat_0=0, resolution='l')

        map.drawcoastlines()
        map.drawcountries()
        map.fillcontinents(color = 'tan')
        map.drawmapboundary()
        
        # Plot groups as medium green dots
        group_x, group_y = map(groups['group_lon'], groups['group_lat'])
        map.plot(group_x, group_y, 'go', markersize=1)
        
        # Plot center of the storm
        storm_center_lon, storm_center_lat = map(row['Long'].values, row['Lat'].values)    
        map.plot(storm_center_lon, storm_center_lat, 'ro', markersize=2)
            
        # Put time 
        props = dict(boxstyle='round', facecolor='wheat', alpha=1)
        plt.annotate(time_str, xy=(1, 1), xytext=(-76, -7.5),
                    xycoords='axes fraction', textcoords='offset points',
                    fontsize=7, bbox=props)
        
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    dataReader = DataReader()
    dataReader.run()