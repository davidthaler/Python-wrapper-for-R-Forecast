from rpy2 import robjects
import pandas as pd
from math import floor

freq = lambda x : robjects.r('frequency')(x)[0]
time = lambda x : list(robjects.r('time')(x))
cycle = lambda x : list(robjects.r('cycle')(x))
  
def mean_prediction(fc):
  '''
  Function to extract the mean prediction from an R forecast.

  Args:
    fc: an object with class forecast from R Forecast

  Returns:
    the mean prediction in a list
  '''
  return list(fc.rx2('mean'))


def prediction_intervals(fc):
  '''
  Function creates a Pandas DataFrame with the upper and lower prediction 
  intervals, as well as the mean prediction.
  
  Args:
    fc: an object with class forecast from R Forecast
    
  Returns:
    a Pandas DataFrame with the mean prediction and prediction intervals
  '''
  mean_fc = list(fc.rx2('mean'))
  idx = get_index(fc.rx2('mean'))
  df = pd.DataFrame({'point_fc' : mean_fc}, index=idx)
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
    idx = get_index(data)
    df = pd.DataFrame(dict(zip(cols, (seasonal, trend, remainder))), index=idx)
    df['data'] = df.sum(axis=1)
    return df[['data', 'seasonal', 'trend', 'remainder']]
  elif cls(decomp)[0] == 'decomposed.ts':
    x = list(decomp.rx2('x'))
    seasonal = list(decomp.rx2('seasonal'))
    trend = list(decomp.rx2('trend'))
    remainder = list(decomp.rx2('random'))
    cols = ['data', 'seasonal', 'trend', 'remainder']
    idx = get_index(decomp.rx2('x'))
    df = pd.DataFrame(dict(zip(cols, (x, seasonal, trend, remainder))), index=idx)
    return df[cols]
  else:
    raise ValueError('Argument must map to an R seasonal decomposition.')


def get_index(ts):
  '''
  Utility function for making the correct argument to constructors for 
  Pandas Series or DataFrame objects so as to get the index to match a 
  given time series.
  
  Args:
    ts: an object that maps to an R time series (class ts)
    
  Returns:
    either a list or a list of lists
  '''
  times = [int(floor(x)) for x in time(ts)]
  cycles = [int(floor(x)) for x in cycle(ts)]
  if freq(ts) > 1:
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
  idx = get_index(ts)
  return pd.Series(ts, index=idx)

   






