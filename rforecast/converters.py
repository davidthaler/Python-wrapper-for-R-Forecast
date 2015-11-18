'''
Converters.py handles conversions between pandas Series with various index 
types and R time series (class 'ts'). It also creates Pandas Series objects 
with the correct index types. Seasonal time series are represented 
as a Pandas Series with a MultiIndex in which the first level is the longer, 
outer time period and the second level is the cycle.
'''
import pandas as pd
import wrappers

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
 return wrappers.ts(x, start=start, frequency=freq)


def _regular_series_as_ts(x):
  '''
  Converts a normally-indexed Pandas Series to an R time series object with 
  the same start period.
  
  Args:
    x: a Pandas Series with a standard index
    
  Returns:
    a non-seasonal R time series.
  '''
  return wrappers.ts(x, start=x.index[0])


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
    return pd.Series(list(x), index=idx)
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
    return pd.Series(data=list(x), index=[outer, inner])














