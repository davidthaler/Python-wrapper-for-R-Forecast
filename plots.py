import matplotlib.pyplot as plt
import pandas as pd
import extractor

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
  s = extractor.ts_as_series(ts)
  s.plot(**kwargs)
  plt.style.use('ggplot')
  plt.show()
  
  
def plot_decomp(decomp, **kwargs):
  '''
  Plots a seasonal decomposition using matplotlib/pyplot/pandas.
  
  Args:
    decomp: an object that maps to a seasonal decomposition in R.
    kwargs: keyword arguments passed through a pandas DataFrame
      and on to pyplot.plot().
      
  Output:
    a plot of the seasonal, trend and remainder components from the 
    decomposition plus the original time series data
  '''
  dcdf = extractor.decomposition(decomp)
  dcdf.plot(subplots=True, **kwargs)
  plt.style.use('ggplot')
  plt.show()


def plot_forecast(fc):
  '''
  Plots a forecast and its prediction intervals.
  
  Args:
    fc: an object that maps to an R forecast

  Output:
    a plot of the series, the mean forecast, and the prediciton intervals
  '''
  plt.style.use('ggplot')
  data = fc.rx2('x')
  data_idx = extractor.time(data)
  plt.plot(data_idx, list(data), color='black')
  mean_fc = fc.rx2('mean')
  fc_idx = extractor.time(mean_fc)
  plt.plot(fc_idx, list(mean_fc), color='blue')
  lower = fc.rx2('lower')
  upper = fc.rx2('upper')
  for (k, level) in enumerate(fc.rx2('level'), 1):
    lower_series = list(lower.rx(True, k))
    upper_series = list(upper.rx(True, k))
    plt.fill_between(fc_idx, lower_series, upper_series, 
                     color='grey', alpha= 0.5/k)
  plt.show()






