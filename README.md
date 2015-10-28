## Python wrapper for R Forecast

*This is work in progress.*

This project uses rpy2 to expose most of the functionality of R's Forecast package in python. 
Some related functions in the stats and base packages are also exposed (e.g. seasonal decompositions).
A few less-commnonly used functions and arguments are not exposed.

An example of generating a forecast:
```
import rpy2.robjects as ro
import wrapper
import extractor

wine = ro.r('wineind')
fc = wrapper.stlf(wine)
result = extractor.prediction_intervals(fc)
print result
```
In the snippet, `wine` maps to an R time series, `fc` maps to an R object with class 'forecast', 
and `result` is a pandas DataFrame.
The data, 'wineind', is imported into R by the forecast package, which is pulled in by the import of wrapper.py. 
In `result`, point_forecast is the mean forecast; lower/upper 80/95 are 80% and 95% prediction interval boundaries.

An example of generating an STL decomposition:
```
dc = wrapper.stl(wine, s_window=7)
result = extractor.decomposition(dc)
print result
```
Usually, the data will be in python to start with. 
To use any of these functions, first get an object that maps to an R time series like this:
```
# A slice of the 'oil' data from R package fpp
data =  [509, 506, 340, 240, 219, 172, 252, 221, 276, 271, 342, 428, 442, 432, 437]
r_ts = wrapper.ts(data, 1980)
```
Then `r_ts` can be used as input for generating forecasts or decompositions.
