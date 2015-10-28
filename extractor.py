from rpy2 import robjects
import pandas as pd


def mean_prediction(fc):
  '''
  Function to extract the mean prediction from an R forecast.

  Args:
    fc - an object with class forecast from R Forecast

  Returns:
    the mean prediction in a list
  '''
  return list(fc.rx2('mean'))


def prediction_intervals(fc):
  '''
  Function creates a Pandas DataFrame with the upper and lower 80% and 
  95% prediction intervals, as well as the mean prediction.
  
  Args:
    fc - an object with class forecast from R Forecast
    
  Returns:
    a Pandas DataFrame with the mean prediction and prediction intervals
  '''
  mean_fc = list(fc.rx2('mean'))
  horizon = len(mean_fc)
  lower_95 = list(fc.rx2('lower')[horizon:])
  lower_80 = list(fc.rx2('lower')[:horizon])
  upper_80 = list(fc.rx2('upper')[:horizon])
  upper_95 = list(fc.rx2('upper')[horizon:])
  results = (lower_95, lower_80, mean_fc, upper_80, upper_95)
  cols = ['lower95', 'lower80', 'point_fc', 'upper80', 'upper95']
  df = pd.DataFrame(dict(zip(cols, results)))
  return df[cols]
  

def decomposition(decomp):
  '''
  Function creates a Pandas DataFrame with the seasonal, trend and remainder 
  components of a seasonal decomposition, along with the original series, in 
  separate columns.
  
  Args:
    decomp - An object that maps to a seasonal decomposition (class 'stl' 
      or 'decomposed.ts' in R), otained from stl or decompose in wrapper.
      
  Returns:
    a Pandas DataFrame with the seasonal, trend and remainder
  '''
  cls = robjects.r('class')
  if cls(decomp)[0] == 'stl':
    data = decomp.rx2('time.series')
    r, c = tuple(data.dim)
    seasonal = list(data[:r])
    trend = list(data[r:(2*r)])
    remainder = list(data[(2*r):(3*r)])
    cols = ['seasonal', 'trend', 'remainder']
    df = pd.DataFrame(dict(zip(cols, (seasonal, trend, remainder))))
    df['data'] = df.sum(axis=1)
    return df[['data', 'seasonal', 'trend', 'remainder']]
  elif cls(decomp)[0] == 'decomposed.ts':
    x = list(decomp.rx2('x'))
    seasonal = list(decomp.rx2('seasonal'))
    trend = list(decomp.rx2('trend'))
    remainder = list(decomp.rx2('random'))
    cols = ['data', 'seasonal', 'trend', 'remainder']
    df = pd.DataFrame(dict(zip(cols, (x, seasonal, trend, remainder))))
    return df[cols]
  else:
    raise ValueError('Argument must map to an R seasonal decomposition.')










