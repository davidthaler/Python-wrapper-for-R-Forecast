from rpy2 import robjects
from rpy2.robjects.packages import importr
import numpy as np
import pandas as pd

forecast = importr('forecast')


def _ts(data, start=1, frequency=1):
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


def _extract_forecast(fc, horizon, mean_only, as_pandas):
  '''
  Utility function to extract the desired elements from a completed forecast 
  and return them as either Python or Pandas objects.
  
  Args:
    fc - a completed forecast
    horizon - number of steps ahead in the forecast
    mean_only - if True, return only the mean prediction.
    as_pandas  - if True, return a Pandas DataFrame or Series
    
  Returns:
    A forecast with or without prediction intervals, as either a list/tuple
    or as a Pandas DataFrame/Series.
  '''
  if mean_only:
    result = list(fc.rx2('mean'))
    if as_pandas:
      return pd.Series(result)
    else: 
      return result
  else:
    lower_95 = list(fc.rx2('lower')[horizon:])
    lower_80 = list(fc.rx2('lower')[:horizon])
    mean_fc  = list(fc.rx2('mean'))
    upper_80 = list(fc.rx2('upper')[:horizon])
    upper_95 = list(fc.rx2('upper')[horizon:])
    results = (lower_95, lower_80, mean_fc, upper_80, upper_95)
    if as_pandas:
      cols = ['lower95','lower80','point_forecast','upper80','upper95']
      df = pd.DataFrame(dict(zip(cols, results)))
      return df[cols]
    else:
      return results

  
def _base_forecast(method, data, start, frequency, 
                  horizon, mean_only, as_pandas):
  '''
  Function for internal use to get a forecast from an R Forecast 
  function with call like:  method(data, horizon). Used for mean, 
  theta, random walk, and naive forecasts.
  
  Args:
    method - a string; name of a forecasting function in R
    data - Python sequence representing values of a regular time series.
    start - a number to use as start index of sequence
    frequency - number of points in each time period.
        e.g. 12 for monthly data with an annual period
    horizon - number of steps ahead to forecast
    mean_only - if True, return only the mean prediction.
    as_pandas  - if True, return a Pandas DataFrame or Series

  Returns:
    A forecast with or without prediction intervals, as either a list/tuple
    or as a Pandas DataFrame/Series.
  '''
  time_series = _ts(data, start=start, frequency=frequency)
  fc_method = robjects.r(method)
  fc = fc_method(time_series, h=horizon)
  return _extract_forecast(fc, horizon, mean_only, as_pandas)


def meanf(data, start=1, frequency=1, horizon=10, 
          mean_only=False, as_pandas=True):
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
    as_pandas  - default True; if True, return a Pandas DataFrame or Series

  Returns:
    A mean forecast with or without prediction intervals, as either 
    a list/tuple or as a Pandas DataFrame/Series.
  '''
  return _base_forecast('meanf', data, start, frequency, 
                       horizon, mean_only, as_pandas)
  
  
def thetaf(data, start=1, frequency=1, horizon=10, 
          mean_only=False, as_pandas=True):
  '''
  Perform a theta forecast on the provided data by calling thetaf() 
  from R Forecast. The theta forecast is equivalent to a random walk 
  forecast (rwf in R Forecast) with drift, with the drift equal to half 
  the slope of a linear regression model fitted to with a trend. The 
  theta forecast did well in the M3 competition.
  
  Args:
    data - Python sequence representing values of a regular time series.
    start - default 1; a number to use as start index of sequence
    frequency - default 1; number of points in each time period.
        e.g. 12 for monthly data with an annual period
    horizon - default 10; number of steps ahead to forecast
    mean_only - default False; if True, return only the mean prediction.
    as_pandas  - default True; if True, return a Pandas DataFrame or Series

  Returns:
    A theta forecast with or without prediction intervals, as either 
    a list/tuple or as a Pandas DataFrame/Series.
  '''
  return _base_forecast('thetaf', data, start, frequency, 
                       horizon, mean_only, as_pandas)


def naive(data, start=1, frequency=1, horizon=10, 
          mean_only=False, as_pandas=True):
  '''
  Perform a naive forecast on the provided data by calling naive() 
  from R Forecast. This is also called the 'Last Observed Value' 
  forecast. The point forecast is a constant at the last observed value.
  
  Args:
    data - Python sequence representing values of a regular time series.
    start - default 1; a number to use as start index of sequence
    frequency - default 1; number of points in each time period.
        e.g. 12 for monthly data with an annual period
    horizon - default 10; number of steps ahead to forecast
    mean_only - default False; if True, return only the mean prediction.
    as_pandas  - default True; if True, return a Pandas DataFrame or Series

  Returns:
    A mean forecast with or without prediction intervals, as either 
    a list/tuple or as a Pandas DataFrame/Series.
  '''
  return _base_forecast('naive', data, start, frequency, 
                       horizon, mean_only, as_pandas)





