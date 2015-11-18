'''
ts_io.py handles reading time series into Pandas Series objects with the 
index set up as used in RForecast.
'''
import pandas as pd


def read_ts(file):
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
  df = pd.read_csv(file, header=None)
  _, ncols = df.shape
  if ncols == 1:
    return pd.Series(df[0].values)
  elif ncols == 2:
    data = df[1].values
    index = df[0].values
    return pd.Series(data=data, index=index)
  elif ncols == 3:
    data = df[2].values
    index = [df[0].values, df[1].values]
    return pd.Series(data=data, index=index)
  else:
    raise IOError('File %s has wrong format' % file)




