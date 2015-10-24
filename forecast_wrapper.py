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
    fc - an object with class forecast from R Forecast
    horizon - number of steps ahead in the forecast
    mean_only - if True, return only the mean prediction.
    as_pandas  - if True, return a Pandas DataFrame or Series
    
  Returns:
    A forecast with or without prediction intervals, 
    as either a list/tuple or as a Pandas DataFrame/Series.
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
                  horizon, mean_only, as_pandas, **kwargs):
  '''
  Function for internal use to get a forecast from an R Forecast 
  function with call like:  method(data, horizon). Used for mean, 
  theta, random walk, and naive forecasts.
  
  It is the caller's responsibility to ensure that any **kwargs 
  are in the signature of the called function.
  
  Args:
    method - a string; name of a forecasting function in R
    data - Python sequence representing values of a regular time series.
    start - a number to use as start index of sequence
    frequency - number of points in each time period.
        e.g. 12 for monthly data with an annual period
    horizon - number of steps ahead to forecast
    mean_only - if True, return only the mean prediction.
    as_pandas  - if True, return a Pandas DataFrame or Series
    kwargs - a dict of name:value pairs for parameters that are specific
        to one of the forecast models. 
        Example: {'drift':True} in an rwf forecast.

  Returns:
    A forecast with or without prediction intervals, as either a list/tuple
    or as a Pandas DataFrame/Series.
  '''
  time_series = _ts(data, start=start, frequency=frequency)
  fc_method = robjects.r(method)
  fc = fc_method(time_series, h=horizon, **kwargs)
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


def snaive(data, start=1, frequency=1, horizon=10, 
          mean_only=False, as_pandas=True):
  '''
  Perform a seasonal naive forecast on the provided data by calling 
  snaive() from R Forecast. This is also called the 'Last Observed 
  Seasonal Value' forecast. The point forecast is the value of the 
  series one full period in the past.
  
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
  return _base_forecast('snaive', data, start, frequency, 
                       horizon, mean_only, as_pandas)


def rwf(data, drift=False, start=1, frequency=1, horizon=10, 
          mean_only=False, as_pandas=True):
  '''
  Perform a random walk forecast on the provided data by calling 
  rwf() from R Forecast. The forecast can have drift, which allows 
  a trend in the mean prediction, but by default, it does not.
  
  Args:
    data - Python sequence representing values of a regular time series.
    drift - default False; if true, allow drift
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
  return _base_forecast('rwf', data, start, frequency, horizon, 
                        mean_only, as_pandas, drift=drift)



