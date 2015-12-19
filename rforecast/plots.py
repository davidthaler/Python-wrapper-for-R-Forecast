'''
The plots module contains functions for producing plots using matplotlib 
of time series, forecast results and seasonal decompositions.
'''
import matplotlib.pyplot as plt
import converters


def plot_ts(ts, **kwargs):
  '''
  Plots an R time series using matplotlib/pyplot/pandas.
  
  Args:
    ts: an object that maps to an R time series
    kwargs: keyword arguments passed through a pandas Series
      and on to pyplot.plot().
    
  Output:
    a time series plot
  '''
  s = converters.to_series(ts)
  s.plot(**kwargs)
  plt.style.use('ggplot')
  plt.show()
  

def plot_decomp(decomp, **kwargs):
  '''
  Plots a seasonal decomposition using matplotlib/pyplot/pandas.
  
  Args:
    decomp: either an R decomposition (class 'stl' or 'decomposed.ts') or 
      a Pandas Data Frame from converters.decomposition.
    kwargs: keyword arguments passed through a pandas DataFrame
      and on to pyplot.plot().
      
  Output:
    a plot of the seasonal, trend and remainder components from the 
    decomposition plus the original time series data
  '''
  decomp = converters.to_decomp(decomp)
  decomp.plot(subplots=True, **kwargs)
  plt.style.use('ggplot')
  plt.show()


def plot_forecast(fc, data=None, test=None, loc='upper left'):
  '''
  Plots a forecast and its prediction intervals.
  
  Args:
    fc: Pandas Data Frame from converters.prediction_intervals,
      or an R forecast object
    data: the data for the forecast period as a Pandas Series, or None 
      if fc is an R forecast
    test: optional data for the forecast period as a Pandas Series
    loc: Default is 'upper left', since plots often go up and right.
      For other values see matplotlib.pyplot.legend().
      
  Output:
    a plot of the series, the mean forecast, and the prediciton intervals, 
    and optionally, the data for the forecast period, if provided,
  '''
  fc, data, test = converters.to_forecast(fc, data, test)
  plt.style.use('ggplot')
  l = list(fc.columns)
  lowers = l[1::2]
  uppers = l[2::2]
  tr_idx = converters.flatten_index(data.index)
  fc_idx = converters.flatten_index(fc.index)
  plt.plot(tr_idx, data, color='black')
  plt.plot(fc_idx, fc[l[0]], color='blue')
  for (k, (low, up)) in enumerate(zip(lowers, uppers), 1):
    plt.fill_between(fc_idx, fc[low], fc[up], color='grey', alpha=0.5/k)
  labels = ['data', 'forecast']
  if test is not None:
    n = min(len(fc.index), len(test))
    plt.plot(fc_idx[:n], list(test[:n]), color='green')
    labels.append('test')
  plt.legend(labels, loc=loc)
  plt.show()    




