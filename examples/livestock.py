'''
This example shows automatic fitting of an arima model with a linear 
trend as a regressor. It is based on a post on Hyndsight, a blog by 
R Forecast package author Rob J. Hyndman.
 
See: http://robjhyndman.com/hyndsight/piecewise-linear-trends/#more-3413
'''
# Not needed if the package is installed
import sys, os
sys.path.append(os.path.abspath('..'))

from rforecast import ts_io
from rforecast import wrappers
from rforecast import converters
from rforecast import plots

# This is how to import data that is installed in R.
stock = ts_io.read_ts('livestock', 'fpp')
n = len(stock)
fc = wrappers.auto_arima(stock, xreg=range(n), newxreg=range(n, n + 10))
print 'Australia livestock population 1961-2007'
print stock
plots.plot_ts(stock)
print '10-year forecast of livestock population'
print fc
plots.plot_forecast(fc, stock)



