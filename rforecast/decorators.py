'''
Module decorators.py holds decorators for transparently converting  
Pandas Series objects that have the correct index for holding a time series 
into R time series objects as they are passed into the forecasting functions 
in wrappers.py.
'''
from rpy2 import robjects
import functools
import converters
import pandas


#TODO: change the type check to full input validation in base_wrap


def wrap_input(func):
  '''
  Wrapper function to convert Pandas series into R ts() object if one is 
  provided. R ts() objects are left alone. This wrapper returns the wrapped 
  function output as-is in either case.
  
  Args:
    func: the wrapped function, must take an R ts object as first argument
    
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
    func: the wrapped function, must take an R ts object as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, converters.ts_as_series)
  
  
def wrap_forecast(func):
  '''
  Wrapper function to convert Pandas series into R ts() object if one is 
  provided. R ts objects are left alone. This function should be used to 
  decorate functions that return an R forecast object normally. If the input 
  is a Pandas Series, then the output is converted to a Pandas Data Frame 
  containing prediction intervals using converters.prediction_intervals(). 
  If the input is an R ts, then the output (an R forecast) is unchanged.
  
  Args:
    func: the wrapped function, must take an R ts object as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, converters.prediction_intervals)


def wrap_decomp(func):
  '''
  Wrapper function to convert Pandas series into R ts object if one is 
  provided. R ts objects are left alone. This function should be used to 
  decorate functions that normally return an R decomposition. If the input 
  is a Pandas Series, then the output is converted to a Pandas Data Frame 
  containing the decomposition using converters.decomposition(). 
  If the input is an R ts, then the output is unchanged.
  
  Args:
    func: the wrapped function, must take an R ts object as first argument
    
  Returns:
    A wrapper function for argument-conversion, to use as a decorator.
  '''
  return base_wrap(func, converters.decomposition)


def base_wrap(func, pandas_func):
  '''
  Wrapper function to convert Pandas series into R ts object if one is 
  provided. R ts objects are left alone. If the input is a Pandas Series, 
  the output is converted using the second argument, pandas_func. 
  If the input is an R ts, then the output is unchanged.
  
  Args:
    func: the wrapped function, must take an R ts object as first argument
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


# The input validation isn't really right here...Its too basic.

def decomp_in(func):
  '''
  Wrapper function to convert R objects of class 'stl' or 'decomposed.ts' to 
  a Pandas Data Frame, if necessary. If a Data Frame is provided, it is 
  passed through unchanged. The wrapped function that is returned has no 
  return value, because this function is intended for plot functions.
  
  Args:
    func: the wrapped function. Takes a Pandas Data Frame like the 
      output from converters.decomposition.

  Returns:
    A wrapper function for argument conversion, to use as a decorator.
  '''
  @functools.wraps(func)
  def inner(*args, **kwargs):
    if type(args[0]) is robjects.ListVector:
      args = list(args)
      args[0] = converters.decomposition(args[0])
    func(*args, **kwargs)
  return inner


def forecast_in(func):
  '''
  Wrapper function to convert an R forecast object into a Pandas Data Frame, 
  with an added Pandas Series containing the data the forecast was generated 
  from, if one is provided. If the Pandas objects are provided, then they are 
  passed through unchanged.
  
  Args:
    func: the wrapped function. Takes a Pandas Data Frame returned from 
      converters.prediction_interval for the first argument, and a Pandas 
      Series with the forecast data as the second.
      
  Returns:
    A wrapper function for argument conversion, to use as a decorator.
  '''
  @functools.wraps(func)
  def inner(*args, **kwargs):
    if type(args[0]) is robjects.ListVector:
      fc = args[0]
      pi = converters.prediction_intervals(fc)
      x = converters.ts_as_series(fc.rx2('x'))
      args = (pi, x)
    func(*args, **kwargs)
  return inner





