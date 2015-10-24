from rpy2 import robjects
from rpy2.robjects.packages import importr
import numpy as np
import pandas as pd

forecast = importr('forecast')


def ts(data, start=1, frequency=1):
  '''
  Utility function to turn input Python sequences into R time series.  
  
  Args:
    data - Python sequence representing values of a regular time series.
    start - default 1; a number to use as start index of sequence
    frequency - default 1; number of points in each time period.
        e.g. 12 for monthly data with an annual period

  Returns:
    an object that maps to an R time series (ts class)
  '''
  ts = robjects.r('ts')
  rdata = robjects.FloatVector(data)
  time_series = ts(rdata, start=start, frequency=frequency)  
  return time_series


def extract_forecast(fc, horizon, mean_only):
  '''
  Utility function to extract the desired elements from a completed forecast.
  
  Args:
    fc - a completed forecast
    horizon - default 10; number of steps ahead in the forecast
    mean_only - default False; if True, return only the mean prediction.
    
  Returns:
    Either the mean forecast as a Python list, or ...         # TODO
  '''
  if mean_only:
    return list(fc.rx2('mean'))
  else:
    cols = ['lower95','lower80','mean_forecast','upper80','upper95']
    lower_95 = list(fc.rx2('lower')[horizon:])
    lower_80 = list(fc.rx2('lower')[:horizon])
    mean_fc  = list(fc.rx2('mean'))
    upper_80 = list(fc.rx2('upper')[:horizon])
    upper_95 = list(fc.rx2('upper')[horizon:])
    return (lower_95, lower_80, mean_fc, upper_80, upper_95)


def meanf(data, start=1, frequency=1, horizon=10, mean_only=False):
  '''
  Perform a mean forecast on the provided data by calling meanf() 
  from R Forecast.
  
  Args:
    data - Python sequence representing values of a regular time series.
    start - default 1; a number to use as start index of sequence
    frequency - default 1; number of points in each time period.
        e.g. 12 for monthly data with an annual period
    horizon - default 10; number of steps ahead to forecast
    mean_only - default False; if True, return only the mean prediction.

  Returns:
    Either the mean forecast as a Python list, or ...         # TODO
  '''
  time_series = ts(data, start=start, frequency=frequency)
  meanf = robjects.r('meanf')
  fc = meanf(time_series, h=horizon)
  return extract_forecast(fc, horizon, mean_only)







