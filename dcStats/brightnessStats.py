import xarray
from datacube_stats.statistics import Percentile, Statistic
from datacube_stats.statistics.uncategorized import PerBandIndexStat
from collections import Sequence
from datacube.model import Measurement
import numpy as np
import pandas as pd


class brightness(Statistic):
    """
       Summary statistics on a 4 band 'Brightness' index: 
               
               sqrt(green^2 + red^2 + nir^2 + swir1^2)
       
       The different statistics are stored as bands in the output GTiff
       """

    def __init__(self, band1, band2, band3, band4, name, stats=None):
        self.stats = stats if stats else ['min', 'max', 'mean']
        self.band1 = band1
        self.band2 = band2
        self.band3 = band3
        self.band4 = band4
        self.name = name

    def compute(self, data):
        nd = (data[self.band1]**2 + data[self.band2]**2 + data[self.band3]**2 + data[self.band4]**2)**(1/2.0)
        outputs = {}
        for stat in self.stats:
            name = '_'.join([self.name, stat])
            outputs[name] = getattr(nd, stat)(dim='time', keep_attrs=True)
        return xarray.Dataset(outputs, attrs=dict(crs=data.crs))   
    
    def measurements(self, input_measurements):
        return [Measurement(name='_'.join([self.name, stat]), dtype='float32', nodata=np.nan, units='1')
                for stat in self.stats] 
    