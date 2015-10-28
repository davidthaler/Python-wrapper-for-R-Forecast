import matplotlib.pyplot as plt
import pandas as pd
import extractor

def plot_ts(ts, **kwargs):
  '''
  Plots an R time series using matplotlib/pyplot/pandas.
  
  Args:
    ts - an object that maps to an R time series
    kwargs - keyword arguments passed through a pandas Series
      and on to pyplot.plot().
    
  Output:
    a time series plot
  '''
  s = pd.Series(list(ts))
  s.plot(**kwargs)
  plt.style.use('ggplot')
  plt.show()
  
  
def plot_decomp(decomp, **kwargs):
  '''
  Plots a seasonal decomposition using matplotlib/pyplot/pandas.
  
  Args:
    decomp - an object that maps to a seasonal decomposition in R.
    kwargs - keyword arguments passed through a pandas DataFrame
      and on to pyplot.plot().
      
  Output:
    a plot of the seasonal, trend and remainder components from the 
    decomposition plus the original time series data
  '''
  dcdf = extractor.decomposition(decomp)
  dcdf.plot(subplots=True, **kwargs)
  plt.style.use('ggplot')
  plt.show()



