'''
ts_io.py handles reading time series into Pandas Series objects with the 
index set up as used in RForecast.
'''
import pandas
import converters
from rpy2 import robjects
from rpy2.robjects.packages import importr


def read_series(file):
  '''
  Function read_ts reads a csv file of a time series. Input file should have 
  1, 2, or 3 columns. If 1 column, it is data-only. If 2-columns, it is read 
  as a non-seasonal timeseries like: time, data. If 3-column, it is read as a 
  seasonal time series, e.g. year, month, data. Seasonal time series will be 
  represented with a Series with a MultiIndex.
  
  Args:
    file: a path or open file to the data
    
  Returns:
    a Pandas Series with the data in the file, and the appropriate type of 
    index for the type of data (seasonal/non-seasonal)
  '''
  df = pandas.read_csv(file, header=None)
  _, ncols = df.shape
  if ncols == 1:
    data = df[0].values
    index = range(1, len(data) + 1)
  elif ncols == 2:
    data = df[1].values
    index = df[0].values
  elif ncols == 3:
    data = df[2].values
    index = [df[0].values, df[1].values]
  else:
    raise IOError('File %s has wrong format' % file)
  return pandas.Series(data=data, index=index)


def read_ts(ts_name, pkgname=None, as_pandas=True):
  '''
  Function reads a time series in from R. If needed, it can load a package 
  containing the time series. The output can be provided as an R object or 
  as a Pandas Series.
  
  Args:
    ts_name: the name of the time series in R
    pkgname: Default None. The name of an R package with the time series.
    as_pandas: Default True. If true, return a Pandas Series.

  Returns:
    the time series as an R time series or a Pandas Series
  '''
  if pkgname is not None:
    importr(pkgname)
  tsout = robjects.r(ts_name)
  return converters.series_out(tsout, as_pandas)





