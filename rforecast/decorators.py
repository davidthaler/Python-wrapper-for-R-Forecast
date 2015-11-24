'''
Module decorators.py holds decorators for transparently converting  
Pandas Series objects that have the correct index for holding a time series 
into R time series objects as they are passed into the forecasting functions 
in wrappers.py.
'''
from rpy2 import robjects
import converters
import extractors
import pandas

#TODO: change the type check to full input validation


def accept_pandas(func):
  def inner(*args, **kwargs):
    if type(args[0]) is pandas.Series:
      args = list(args)
      args[0] = converters.series_as_ts(args[0])
    return func(*args, **kwargs)
  return inner
  

def wrap_forecast(func):
  def inner(*args, **kwargs):
    is_pandas = False
    if type(args[0]) is pandas.Series:
      is_pandas = True
      args = list(args)
      args[0] = converters.series_as_ts(args[0])
    fc = func(*args, **kwargs)
    if is_pandas:
      return extractors.prediction_intervals(fc)
    else:
      return fc
  return inner
  

def wrap_decomp(func):
  def inner(*args, **kwargs):
    is_pandas = False
    if type(args[0]) is pandas.Series:
      is_pandas = True
      args = list(args)
      args[0] = converters.series_as_ts(args[0])
    dc = func(*args, **kwargs)
    if is_pandas:
      return extractors.decomposition(dc)
    else:
      return dc
  return inner










