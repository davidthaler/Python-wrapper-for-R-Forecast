'''
Converters.py handles conversions between pandas Series with various index 
types and R time series (class 'ts'). It also creates Pandas Series objects 
with the correct index types. Seasonal time series are represented 
as a Pandas Series with a MultiIndex in which the first level is the longer, 
outer time period and the second level is the cycle.
'''
import pandas
from rpy2.robjects.packages import importr
from rpy2 import robjects


stats = importr('stats')


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














