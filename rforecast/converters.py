'''
Converters.py handles conversions between pandas Series with various index 
types and R time series (class 'ts'). It also creates Pandas Series objects 
with the correct index types. Seasonal time series are represented 
as a Pandas Series with a MultiIndex in which the first level is the longer, 
outer time period and the second level is the cycle.
'''
import numpy
import pandas
from rpy2.robjects.packages import importr
from rpy2 import robjects
from math import floor


stats = importr('stats')


# TODO: input validation isn't really right here


def to_ts(x):
  if type(x) is pandas.Series:
    return series_as_ts(x), True
  else:
    return x, False
  
  
def series_out(x, is_pandas):
  if is_pandas:
    return ts_as_series(x)
  else:
    return x
    
    
def forecast_out(fc, is_pandas):
  if is_pandas:
    return prediction_intervals(fc)
  else:
    return fc
    
    
def decomposition_out(dc, is_pandas):
  if is_pandas:
    return decomposition(dc)
  else: 
    return dc


def to_series(x):
  if type(x) is pandas.Series:
    return x
  else:
    return ts_as_series(x)


def to_decomp(dc):
  if type(dc) is pandas.DataFrame:
    return dc
  else:
    return decomposition(dc)
    
def to_forecast(fc, data, test):
  if test is not None:
    test = to_series(test)
  if type(fc) is pandas.DataFrame:
    if type(data) is not pandas.Series:
      raise ValueError(
        'If forecast is Pandas Data Frame, data must be Pandas Series')
    return fc, data, test
  else:
    pi = prediction_intervals(fc)
    x = ts_as_series(fc.rx2('x'))
    return pi, x, test

def matrix(x):
  '''
  Converts Python data to an R matrix. This function converts lists, 1-D 
  numpy arrays and Pandas Series to a 1-column matrix. Pandas DataFrames 
  and numpy 2-D arrays are converted to an R matrix with the same shape.
  Forecast methods that allow regressors, like Arima or auto.arima, 
  take them as an R matrix. 
  
  Args:
    x: a list, numpy ndarray (1-D or 2-D), Pandas Series or DataFrame
    
  Returns:
    an R matrix containing x
  '''
  nrow = len(x)
  if type(x) is pandas.DataFrame:
    x = x.values.ravel()
  if type(x) is numpy.ndarray:
    x = x.ravel()
  rdata = robjects.FloatVector(x)
  return robjects.r.matrix(rdata, byrow=True, nrow=nrow)
  
  
def map_arg(x):
  '''
  Many arguments in R may be either numbers or vectors. Rpy2 translates 
  arguments that are numbers automatically, but does not translate tuples 
  or lists to R vectors. This function translates tuples or lists to R 
  vectors, if needed.
  
  Args:
    x: a number or list/tuple
    
  Returns:
    either an R vector containing the values in x, or the number x
  '''
  if type(x) in (tuple, list):
    return robjects.r.c(*x)
  else:
    return x


def translate_kwargs(**kwargs):
  '''
  Translates between python and R keyword arguments. 
  First, tuple arguments are rewritten to R vectors. Next, substitution 
  is performed for a specific list of arguments. Currently, this is just 
  'lam' -> 'lambda'; 'lambda' is a reserved word in python, but is used 
  a lot in the R Forecast package. Finally, underscore-separated keywords 
  are turned into R-style, dot-separated ones. If you need to pass an R 
  argument that has an underscore, you must put it into the 'reserved' dict.
  
  Args:
    **kwargs: the dict of all keyword arguments to a python function
    
  Returns:
    A dict that can be passed as **kwargs to R functions
  '''
  reserved = {'lam':'lambda'}
  for key in kwargs:
    if type(kwargs[key]) in (list, tuple):
      kwargs[key] = robjects.r.c(*kwargs[key])
    if key in reserved:
      kwargs[reserved[key]] = kwargs[key]
      del kwargs[key]
    elif '_' in key:
      new_key = key.replace('_', '.')
      kwargs[new_key] = kwargs[key]
      del kwargs[key]
  return kwargs
  

def ts(data, **kwargs):
  '''
  Turns the provided data into an R time series. Only one of frequency and 
  deltat should be given. If both of start and end are specified, truncation 
  or recycling may occur, which is usually not sensible.
  
  Args:
    data: Python sequence representing values of a regular time series.
    start: default 1; a number or 2-tuple to use as start index of sequence.
      If 2-tuple, it is (period, step), e.g. March 2010 is (2010, 3).
    end: By default this is not specified, which is usually right. 
      A number or 2-tuple (like start) to specify the end of the sequence.
    frequency: default 1; number of points in each time period
      e.g. 12 for monthly data with an annual period
    deltat: default 1; fraction of sampling period per observation 
      e.g. 1/12 for monthly data with an annual period. Only one of deltat 
      and frequency should be defined.

  Returns:
    an object containing the data that maps to an R time series (class 'ts')
  '''
  rdata = robjects.FloatVector(data)
  kwargs = translate_kwargs(**kwargs)
  time_series = stats.ts(rdata, **kwargs)
  return time_series


def _get_index(ts):
  '''
  Utility function for making the correct argument to constructors for 
  Pandas Series or DataFrame objects so as to get the index to match a 
  given time series.
  
  Args:
    ts: an object that maps to an R time series (class ts)
    
  Returns:
    either a list or a list of lists
  '''
  times = [int(floor(x)) for x in list(robjects.r('time')(ts))]
  cycles = [int(x) for x in list(robjects.r('cycle')(ts))]
  if robjects.r('frequency')(ts)[0] > 1:
    return [times, cycles]
  else:
    return times 
  

def ts_as_series(ts):
  '''
  Convert an R time series into a Pandas Series with the appropriate 
  (seasonal/non-seasonal) index.
  
  Args:
    ts: an object that maps to an R time series (class ts)
    
  Returns:
    a Pandas Series with the same data and index as ts
  '''
  idx = _get_index(ts)
  return pandas.Series(ts, index=idx)


  
def _seasonal_series_as_ts(x):
 '''
 Converts a Pandas Series with a MultiIndex into a seasonal R time series.
 The MultiIndex should only ever be used to represent seasonal series.
 
 Args:
   x: a Pandas Series with a MultiIndex
   
  Returns:
    an R seasonal time series
 ''' 
 idx = x.index
 start = idx[0]
 freq = len(idx.levels[1])
 return ts(x, start=start, frequency=freq)


def _regular_series_as_ts(x):
  '''
  Converts a normally-indexed Pandas Series to an R time series object with 
  the same start period.
  
  Args:
    x: a Pandas Series with a standard index
    
  Returns:
    a non-seasonal R time series.
  '''
  return ts(x, start=x.index[0])


def series_as_ts(x):
  '''
  Takes a Pandas Series with either a seasonal or non-seasonal time series 
  in it, and converts it to an R time series (class 'ts'). If the series is 
  seasonal, x must have a MultiIndex encoding the inner and outer period. 
  If it is non-seasonal, x must have an ordinary index with the periods.
  
  Args:
    x: a Pandas Series
    
  Returns:
    an R time series
  '''
  if x.index.nlevels == 2:
    return _seasonal_series_as_ts(x)
  else:
    return _regular_series_as_ts(x)


# TODO: this need some arg-checking
def sequence_as_series(x, start=1, freq=1):
  '''
  Converts a list or other sequence input into a Pandas Series with the 
  correct index for the type of Series created.
  
  Args:
    x: a time series as a Python list, Pandas Series or numpy ndarray (1-D)
    start: default 1; a number or 2-tuple to use as start index of sequence.
      If 2-tuple, it is (period, step), e.g. March 2010 is (2010, 3).
    freq: default 1; number of points in each time period
      e.g. 12 for monthly data with an annual period
    
  Returns:
    a Pandas Series with the correct index for the time series
  '''
  if freq <= 1:
    idx = range(start, start + len(x))
    return pandas.Series(list(x), index=idx)
  else:
    if type(start) not in (list, tuple):
      start = (start, 1)
    i, j = start
    inner = []
    outer = []
    for k in range(len(x)):
      inner.append(j)
      outer.append(i)
      j += 1
      if j > freq:
        i += 1
        j = 1
    return pandas.Series(data=list(x), index=[outer, inner])


def prediction_intervals(fc):
  '''
  Function creates a Pandas DataFrame with the upper and lower prediction 
  intervals, as well as the mean prediction.
  
  Args:
    fc: an object with class forecast from R Forecast
    
  Returns:
    a Pandas DataFrame with the mean prediction and prediction intervals
  '''
  if robjects.r('class')(fc)[0] != 'forecast':
    raise ValueError('Argument must map to an R forecast.')
  mean_fc = list(fc.rx2('mean'))
  idx = _get_index(fc.rx2('mean'))
  df = pandas.DataFrame({'point_fc' : mean_fc}, index=idx)
  colnames = ['point_fc']
  lower = fc.rx2('lower')
  upper = fc.rx2('upper')
  for (k, level) in enumerate(fc.rx2('level'), 1):
    lower_colname = 'lower%d' % level
    df[lower_colname] = lower.rx(True, k)
    colnames.append(lower_colname)
    upper_colname = 'upper%d' % level
    df[upper_colname] = upper.rx(True, k)
    colnames.append(upper_colname)
  return df[colnames]


def accuracy(acc):
  '''
  Convert the R matrix of forecast accuracy measures returned from 
  wrappers.accuracy into a Pandas DataFrame.
  
  Args:
    acc: R matrix returned from wrappers.accuracy
    
  Returns:
    Pandas DataFrame with accuracy measures
  '''
  index = pandas.Index(list(acc.colnames))
  if acc.dim[0] == 2:
    data = {'Train' : list(acc)[::2]}
    data['Test'] = list(acc)[1::2]
  else:
    data = {'Train' : list(acc)}
  return pandas.DataFrame(data=data, index=index)


def decomposition(decomp):
  '''
  Function creates a Pandas DataFrame with the seasonal, trend and remainder 
  components of a seasonal decomposition, along with the original series, in 
  separate columns.
  
  Args:
    decomp: An object that maps to a seasonal decomposition (class 'stl' 
      or 'decomposed.ts' in R), otained from stl or decompose in wrapper.
      
  Returns:
    a Pandas DataFrame with the seasonal, trend and remainder
  '''
  cls = robjects.r('class')
  if cls(decomp)[0] == 'stl':
    data = decomp.rx2('time.series')
    seasonal = list(data.rx(True, 1))
    trend = list(data.rx(True, 2))
    remainder = list(data.rx(True, 3))
    cols = ['seasonal', 'trend', 'remainder']
    idx = _get_index(data)
    df = pandas.DataFrame(dict(zip(cols, (seasonal, trend, remainder))), index=idx)
    df['data'] = df.sum(axis=1)
    return df[['data', 'seasonal', 'trend', 'remainder']]
  elif cls(decomp)[0] == 'decomposed.ts':
    x = list(decomp.rx2('x'))
    seasonal = list(decomp.rx2('seasonal'))
    trend = list(decomp.rx2('trend'))
    remainder = list(decomp.rx2('random'))
    cols = ['data', 'seasonal', 'trend', 'remainder']
    idx = _get_index(decomp.rx2('x'))
    df = pandas.DataFrame(dict(zip(cols, (x, seasonal, trend, remainder))), index=idx)
    return df[cols]
  else:
    raise ValueError('Argument must map to an R seasonal decomposition.')







