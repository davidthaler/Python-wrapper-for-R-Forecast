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
  











