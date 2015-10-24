from rpy2 import robjects
from rpy2.robjects.packages import importr

forecast = importr('forecast')

def mean_forecast(data, start=1, frequency=1, horizon=10, mean_only=False):
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
  ts = robjects.r('ts')
  rdata = robjects.FloatVector(data)
  time_series = ts(rdata, start=start, frequency=frequency)
  meanf = robjects.r('meanf')
  fc = meanf(time_series, h=horizon)
  if mean_only:
    return list(fc.rx2('mean'))
  else:
    lower_95 = list(fc.rx2('lower')[horizon:])
    lower_80 = list(fc.rx2('lower')[:horizon])
    mean_fc  = list(fc.rx2('mean'))
    upper_80 = list(fc.rx2('upper')[:horizon])
    upper_95 = list(fc.rx2('upper')[horizon:])
    return (lower_95, lower_80, mean_fc, upper_80, upper_95)