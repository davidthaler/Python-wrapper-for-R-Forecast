'''
The extractors module contains functions for converting forecasts or 
seasonal decompositions (R objects) into python objects, primarily 
Pandas DataFrames.
'''

from rpy2 import robjects
import pandas as pd
from math import floor


def mean_prediction(fc):
  '''
  Function to extract the mean prediction from an R forecast.

  Args:
    fc: an object with class forecast from R Forecast

  Returns:
    the mean prediction in a list
  '''
  return list(fc.rx2('mean'))



  




   






