'''
This example shows automatic fitting of an arima model with a linear 
trend as a regressor. It is based on a post on Hyndsight, a blog by 
R Forecast package author Rob J. Hyndman.
 
See: http://robjhyndman.com/hyndsight/piecewise-linear-trends/#more-3413
'''
from rforecast import ts_io
from rforecast import wrappers
from rforecast import converters
from rforecast import plots

stock = ts_io.read_ts('livestock', 'fpp')
n = len(stock)
xreg = converters.matrix(range(n))
newxreg = converters.matrix(range(n, n + 10))
fc = wrappers.auto_arima(stock, xreg=xreg, newxreg=newxreg)
print fc
plots.plot_forecast(fc)