'''
Module decorators.py holds decorators for transparently converting  
Pandas Series objects that have the correct index for holding a time series 
into R time series objects as they are passed into the forecasting functions 
in wrappers.py.
'''
from rpy2 import robjects
import functools
import converters
import extractors
import pandas


#TODO: change the type check to full input validation in base_wrap


def wrap_input(func):
  '''
  Wrapper function to convert Pandas series into R ts() object if one is 
  provided. R ts() objects are left alone. This wrapper returns the wrapped 
  function output as-is in either case.
  
  Args:
    func: the wrapped function, must take ts or Pandas Series as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, lambda x : x)


def wrap_series(func):
  '''
  Wrapper function to convert Pandas series into R ts() object if one is 
  provided. R ts objects are left alone. This function should be used to 
  decorate functions that return an R ts normally. If the input is a Pandas 
  Series, then the output is converted back to a Pandas Series. If the input 
  is an R ts object, then the output is left alone.
  
  Args:
    func: the wrapped function, must take ts or Pandas Series as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, extractors.ts_as_series)
  
  
def wrap_forecast(func):
  '''
  Wrapper function to convert Pandas series into R ts() object if one is 
  provided. R ts objects are left alone. This function should be used to 
  decorate functions that return an R forecast object normally. If the input 
  is a Pandas Series, then the output is converted to a Pandas Data Frame 
  containing prediction intervals using extractors.prediction_intervals(). 
  If the input is an R ts, then the output (an R forecast) is unchanged.
  
  Args:
    func: the wrapped function, must take ts or Pandas Series as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, extractors.prediction_intervals)


def wrap_decomp(func):
  '''
  Wrapper function to convert Pandas series into R ts object if one is 
  provided. R ts objects are left alone. This function should be used to 
  decorate functions that normally return an R decomposition. If the input 
  is a Pandas Series, then the output is converted to a Pandas Data Frame 
  containing the decomposition using extractors.decomposition(). 
  If the input is an R ts, then the output is unchanged.
  
  Args:
    func: the wrapped function, must take ts or Pandas Series as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, extractors.decomposition)


def base_wrap(func, pandas_func):
  '''
  Wrapper function to convert Pandas series into R ts object if one is 
  provided. R ts objects are left alone. If the input is a Pandas Series, 
  the output is converted using the second argument, pandas_func. 
  If the input is an R ts, then the output is unchanged.
  
  Args:
    func: the wrapped function, must take ts or Pandas Series as first argument
    pandas_func: the function to call to convert the output
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  @functools.wraps(func)
  def inner(*args, **kwargs):
    is_pandas = False
    if type(args[0]) is pandas.Series:
      is_pandas = True
      args = list(args)
      args[0] = converters.series_as_ts(args[0])
    out = func(*args, **kwargs)
    if is_pandas:
      return pandas_func(out)
    else:
      return out
  return inner



    



