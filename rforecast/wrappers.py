'''
The wrappers module contains functions that wrap forecasting functions and 
seasonal decompositions from R. It is the main module in this package.
'''
from rpy2 import robjects
from rpy2.robjects.packages import importr
import numpy
import pandas
import converters


fc = importr('forecast')
stats = importr('stats')
NULL = robjects.NULL
NA = robjects.NA_Real


def frequency(x):
  '''
  Function returns the frequency attribute of an R time series. 
  This should be  1 if the series is non-periodic. Otherwise, it should be 
  the number of data points in one period, e.g. 12 for monthly data. 
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
  Returns:
    The number of data points per period in x, as a single float
  '''
  x, _ = converters.to_ts(x)
  return stats.frequency(x)[0]
  

def _get_horizon(x, h=None):
  '''
  Utility function for getting forecast horizons.
  
  Args:
    x: the R time series to be forecast
    h: None, or a forecast horizon
    
  Returns:
    the provided h value, or the correct default if h is None
  '''
  if h is not None:
    return h
  if frequency(x) > 1:
    return 2 * frequency(x)
  else:
    return 10


def meanf(x, h=10, level=(80,95), lam=NULL):
  '''
  Perform a mean forecast on the provided data by calling meanf() 
  from R Forecast.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: default 10; the forecast horizon.
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  level = converters.map_arg(level)
  out = fc.meanf(x, h, level=level, **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)
  

def thetaf(x, h=10, level=(80, 95)):
  '''
  Perform a theta forecast on the provided data by calling thetaf() 
  from R Forecast. The theta forecast is equivalent to a random walk 
  forecast (rwf in R Forecast) with drift, with the drift equal to half 
  the slope of a linear regression model fitted to with a trend. The 
  theta forecast did well in the M3 competition.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: default 10; the forecast horizon.
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
      
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  level = converters.map_arg(level)
  out = fc.thetaf(x, h, level=level)
  return converters.forecast_out(out, is_pandas)


def naive(x, h=10, level=(80, 95), lam=NULL):
  '''
  Perform a naive forecast on the provided data by calling naive() 
  from R Forecast. This is also called the 'Last Observed Value' 
  forecast. The point forecast is a constant at the last observed value.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: default 10; the forecast horizon.
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  level = converters.map_arg(level)
  out = fc.naive(x, h, level=level, **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)
  

def snaive(x, h=None, level=(80, 95), lam=NULL):
  '''
  Perform a seasonal naive forecast on the provided data by calling 
  snaive() from R Forecast. This is also called the 'Last Observed 
  Seasonal Value' forecast. The point forecast is the value of the 
  series one full period in the past.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
      For this forecast method, x should be seasonal.
    h: Forecast horizon; default is 2 full periods of a periodic series
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  h = _get_horizon(x, h)
  level = converters.map_arg(level)
  out = fc.snaive(x, h, level=level, **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)
  

def rwf(x, h=10, drift=False, level=(80, 95), lam=NULL):
  '''
  Perform a random walk forecast on the provided data by calling 
  rwf() from R Forecast. The forecast can have drift, which allows 
  a trend in the mean prediction, but by default, it does not.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: default 10; the forecast horizon.
    drift: default False. If True, a random walk with drift model is fitted.
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  level = converters.map_arg(level)
  out = fc.rwf(x, h, drift, level=level, **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)


def ses(x, h=10, level=(80, 95), alpha=NULL, lam=NULL):
  '''
  Generate a simple exponential smoothing forecast for the time series x.
  This function does not optimize the initial value. To get an optimal 
  initial value, use ets() with model_spec='ANN'.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: the forecast horizon, default 10
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    alpha: exponential smoothing parameter. Must be a float value between 
      0.0001 and 0.9999 or R's NULL value (the default), in which
      case this parameter is optimized.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.
  
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  if alpha is not NULL:
    if alpha < 0.0001 or alpha > 0.9999:
      raise ValueError('alpha must be between 0.0001 and 0.9999, if given')
  x, is_pandas = converters.to_ts(x)
  level = converters.map_arg(level)
  out = fc.ses(x, h, level=level, alpha=alpha, 
                     initial='simple', **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)


def holt(x, h=10, level=(80, 95), alpha=NULL, beta=NULL, lam=NULL):
  '''
  Generates a forecast using Holt's exponential smoothing method.
  Initial values are fitted from the first values in x. For optimized values, 
  use ets() with model_spec='AAN'.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: the forecast horizon, default 10
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    alpha: level smoothing parameter. Must be a float value between 
      0.0001 and 0.9999 or R's NULL value (the default), in which
      case this parameter is optimized.
    beta: trend smoothing parameter. Must be a float value between 
      0.0001 and 0.9999 or R's NULL value (the default), in which
      case this parameter is optimized.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  if alpha is not NULL:
    if alpha < 0.0001 or alpha > 0.9999:
      raise ValueError('alpha must be between 0.0001 and 0.9999, if given')
  if beta is not NULL:
    if beta < 0.0001 or beta > 0.9999:
      raise ValueError('beta must be between 0.0001 and 0.9999, if given')
  x, is_pandas = converters.to_ts(x)
  level = converters.map_arg(level)
  out = fc.holt(x, h, level=level, alpha=alpha, beta=beta, 
               initial='simple', **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)


def hw(x, h=None, level=(80, 95), alpha=NULL, beta=NULL, gamma=NULL, lam=NULL):
  '''
  Generates a forecast using Holt-Winter's exponential smoothing.
  Initial values are fitted from the first values in x. For optimized values, 
  use ets() with model_spec='AAA'.

  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: the forecast horizon
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    alpha: level smoothing parameter. Must be a float value between 
      0.0001 and 0.9999 or R's NULL value (the default), in which
      case this parameter is optimized.
    beta: trend smoothing parameter. Must be a float value between 
      0.0001 and 0.9999 or R's NULL value (the default), in which
      case this parameter is optimized.
    gamma: seasonal smoothing parameter. Must be a float value between 
      0.0001 and 0.9999 or R's NULL value (the default), in which
      case this parameter is optimized.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.

  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  if alpha is not NULL:
    if alpha < 0.0001 or alpha > 0.9999:
      raise ValueError('alpha must be between 0.0001 and 0.9999, if given')
  if beta is not NULL:
    if beta < 0.0001 or beta > 0.9999:
      raise ValueError('beta must be between 0.0001 and 0.9999, if given')
  if gamma is not NULL:
    if gamma < 0.0001 or gamma > 0.9999:
      raise ValueError('gamma must be between 0.0001 and 0.9999, if given')
  x, is_pandas = converters.to_ts(x)
  h = _get_horizon(x, h)
  level = converters.map_arg(level)
  out = fc.hw(x, h, level=level, alpha=alpha, beta=beta, gamma=gamma, 
              initial='simple', **{'lambda' : lam})
  return converters.forecast_out(out, is_pandas)


def forecast(x, h=None, **kwargs):
  '''
  Generate a forecast for the time series x, using ets if x is non-seasonal 
  or has frequency less than 13, and stlf if x is periodic with frequency 
  above 13.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: the forecast horizon
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    robust: Default False. If True, missing values are filled before 
      forecasting and outliers are identified and replaced with tsclean().
    lam : BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.
    find_frequency: Default False. If True, function will try to determine 
      the series frequency from the data.
    allow_multiplicative_trend: Default is False. If True, consider models 
      with a multiplicative trend component. That type of model may grow 
      explosively.
        
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  h = _get_horizon(x, h)
  kwargs = converters.translate_kwargs(**kwargs)
  out = fc.forecast(x, h=h, **kwargs)
  return converters.forecast_out(out, is_pandas)


def ets(x, h=None, model_spec='ZZZ', damped=NULL, alpha=NULL, 
        beta=NULL, gamma=NULL, phi=NULL, additive_only=False, lam=NULL,
        opt_crit='lik', nmse=3, ic='aicc', allow_multiplicative_trend=False,
        level=(80, 95)):
  '''
  Automatically select and fit an exponential smoothing model on the 
  provided data using the ets() function from the R Forecast package, 
  and use it to produce a forecast over the given horizon.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h:  Forecast horizon; default is 2 full periods of a periodic series,
        or 10 steps for non-seasonal series.
    model_spec : Default is 'ZZZ'. A 3-letter string denoting the model type.
        Letters denote error, trend, and seasonal parts: A=additive, 
        N=none, M=multiplicative, Z=automatically selected. Legal 
        values for first part are (A, M, Z), all values are legal 
        for other parts.
    damped : If True, use a damped trend model. 
        Default is NULL, which tries damped/undamped models and 
        selects best model according to the selected ic.
    alpha : Smoothing parameter for error term. 
        Default is NULL, which fits this value.
    beta : Smoothing paramter for trend component. 
        Default is NULL, which fits this value.
    gamma : Smoothing parameter for seasonal component. 
        Default is NULL, which fits this value.
    phi : Damping parameter. Default is NULL, which fits this value.
    additive_only : Default False. If True, only try additive models.
    lam : BoxCox transformation parameter. The default is R's NULL value.
        If NULL, no transformation is applied. Otherwise, a Box-Cox 
        transformation is applied before forecasting and inverted after.
    opt_crit : Optimization criterion. Default is 'lik' for log-likelihood. 
        Other values are 'mse' (mean squared error), 'amse' (MSE averaged 
        over first nmse forecast horizons), 'sigma' (standard deviation of 
        residuals), and 'mae' (mean absolute error).
    nmse : number of steps in average MSE, if 'amse' is opt_crit.
        Restricted to 1 <= nmse <= 10.
    ic : information crierion. Default is 'aicc' for bias-corrected AIC.
        Other values are 'aic' for regular AIC, or 'bic' for BIC.
    allow_multiplicative_trend : Default is False. If True, consider models 
        with a multiplicative trend component. That type of model may grow 
        explosively.
    level : A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
        
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  kwargs = {'allow.multiplicative.trend' : allow_multiplicative_trend, 
            'additive.only' : additive_only, 
            'opt.crit' : opt_crit,
            'lambda' : lam}
  ets_model = fc.ets(x, model=model_spec, damped=damped, alpha=alpha, 
                       beta=beta, gamma=gamma, phi=phi, ic=ic, **kwargs)
  h = _get_horizon(x, h)
  level = converters.map_arg(level)
  # NB: default lambda is correct - it will be taken from model
  out = fc.forecast_ets(ets_model, h, level=level)
  return converters.forecast_out(out, is_pandas)
  
  
def arima(x, h=None, level=(80,95), order=(0,0,0), seasonal=(0,0,0), 
         lam=NULL, **kwargs):
  '''
  Generates a forecast from an arima model with a fixed specification.
  For an arima model with an optimized specification, use auto.arima.
  Keyword arguments are allowed. Some common ones are noted below.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h: the forecast horizon, default 10 if fitting a non-seasonal model,
      2 * the frequency of the series for seasonal models.
    level: A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
    order: the non-seasonal part of the arima model
    seasonal: the seasonal part of the arima model
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.
  
  Keyword Args:
    include_drift: Default False. If True, the model includes a linear 
      drift term
    include_mean: Should the model allow a non-zero mean term?
      Default is True if series is undifferenced, False otherwise
    include_constant: If True, include mean if series is not differenced,
      or include drift if it is differenced once.
    
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  if h is None:
    if seasonal == (0,0,0):
      h = 10
    else:
      h = 2 * frequency(x)
  level = converters.map_arg(level)
  order = converters.map_arg(order)
  seasonal = converters.map_arg(seasonal)
  kwargs['lambda'] = lam
  model = fc.Arima(x, order=order, seasonal=seasonal, **kwargs)
  out = fc.forecast(model, h=h, level=level)
  return converters.forecast_out(out, is_pandas)
   

# TODO: convert xreg and newxreg if needed
def auto_arima(x, h=None, d=NA, D=NA, max_p=5, max_q=5, max_P=2, max_Q=2,
               max_order=5, max_d=2, max_D=1, start_p=2, start_q=2, 
               start_P=1, start_Q=1, stationary=False, seasonal=True, 
               ic='aicc', xreg=NULL, newxreg=NULL, test='kpss', 
               seasonal_test='ocsb', lam=NULL, level=(80, 95)):
  '''
  Use the auto.arima function from the R Forecast package to automatically 
  select an arima model order, fit the model to the provided data, and 
  generate a forecast.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    h : Forecast horizon; default is 2 full periods of a periodic series,
        or 10 steps for non-seasonal series.
    d : order of first differencing. Default is NA, which selects this 
        value based on the value of 'test' (KPSS test by default).
    D : order of seasonal differencing. Default is NA, which selects this 
        value based on 'seasonal_test' (OCSB test by default).
    max_p : maximum value for non-seasonal AR order
    max_q : maximum value for non-seasonal MA order
    max_P : maximum value for seasonal AR order
    max_Q : maximum value for seasonal MA order
    max_order : maximum value of p + q + P + Q
    start_p : starting value for non-seasonal AR order
    start_q : starting value for non-seasonal MA order
    start_P : starting value for seasonal AR order
    start_Q : starting value for seasonal MA order
    stationary : Default is False. If True, only consider stationary models.
    seasonal : Default is True. If False, only consider non-seasonal models.
    ic : information crierion. Default is 'aicc' for bias-corrected AIC.
        Other values are 'aic' for regular AIC, or 'bic' for BIC.
    xreg : An optional vector or matrix of regressors, which must have one 
        row/element for each point in x. Default is NULL, for no regressors.
    newxreg : If regressors were used to fit the model, then they must be 
        supplied for the forecast period as newxreg. If newxreg is present,
        h is ignored.
    test : Test to use to determine number of first differences. Default 
        is 'kpss', for the KPSS test. Other values are 'adf' for augmented 
        Dickey-Fuller, or 'pp' for Phillips-Perron.
    seasonal_test : Test to use to determine number of seasonal differences.
        Default is 'ocsb' for the Osborn-Chui-Smith-Birchenhall  test. 
        The alternative is 'ch' for the Canova-Hansen test. 
    lam : BoxCox transformation parameter. The default is R's NULL value.
        If NULL, no transformation is applied. Otherwise, a Box-Cox 
        transformation is applied before forecasting and inverted after.
    level : A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
      
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  kwargs = {'max.p' : max_p, 'max.q' : max_q, 'max.P' : max_P, 
            'max.Q' : max_Q, 'max.order' : max_order, 'max.d' : max_d, 
            'max.D' : max_D, 'start.p' : start_p, 'start.q' : start_q, 
            'start.P' : start_P, 'start.Q' : start_Q, 
            'seasonal.test' : seasonal_test, 'lambda' : lam}
  if (xreg is NULL) != (newxreg is NULL):
    raise ValueError(
        'Specifiy both xreg and newxreg or neither.')
  if xreg is not NULL:
    xreg = converters.as_matrix(xreg)
    newxreg = converters.as_matrix(newxreg)
  arima_model = fc.auto_arima(x, d=d, D=D, stationary=stationary, 
                                    seasonal=seasonal, ic=ic, xreg=xreg, 
                                    test=test, **kwargs)
  h = _get_horizon(x, h)
  level = converters.map_arg(level)
  # NB: default lambda is correct - it will be taken from model
  out = fc.forecast_Arima(arima_model, h, level=level, xreg=newxreg)
  return converters.forecast_out(out, is_pandas)


def stlf(x, h=None, s_window=7, robust=False, lam=NULL, method='ets', 
         etsmodel='ZZZ', xreg=NULL, newxreg=NULL, level=(80, 95)):
  '''
  Constructs a forecast of a seasonal time series by seasonally decomposing 
  it using an STL decomposition, then making a non-seasonal forecast on the 
  seasonally adjusted data, and finally adding the naively extended seasonal 
  component on to the forecast.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
      For this forecast method, x should be seasonal.
    h : Forecast horizon; default is 2 full periods of a periodic series
    s.window : either 'periodic' or the span (in lags) of the 
      loess window for seasonal extraction, which should be odd.
    robust : If True, use robust fitting in the loess procedure.
    lam : BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.
    method : One of 'ets' or 'arima'; default is 'ets'. Specifies the type 
      of model to use for forecasting the non-seasonal part.
    etsmodel : Default is 'ZZZ'. This is only used if 'method' is 'ets'.
      A 3-letter string denoting the ets model type.
      Letters denote error, trend, and seasonal parts: A=additive, 
      N=none, M=multiplicative, Z=automatically selected. Legal 
      values for first part are (A, M, Z), all values are legal 
      for other parts.
    xreg : Only available if 'method' is arima. An optional vector or matrix 
      of regressors, which must have one row/element for each point in x. 
      Default is NULL, for no regressors.
    newxreg : Only available if 'method' is arima. If regressors are used in 
      fitting, then they must be supplied for the forecast period as newxreg.
    level : A number or list/tuple of prediction interval confidence values.
      Default is 80% and 95% intervals.
      
  Returns:
    If x is an R ts object, an R forecast is returned. If x is a Pandas 
    Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  h = _get_horizon(x, h)
  kwargs = {'s.window' : s_window,
            'lambda' : lam}
  level = converters.map_arg(level)
  out = fc.stlf(x, h, level=level, robust=robust, method=method, 
                       etsmodel=etsmodel, xreg=xreg, newxreg=newxreg, **kwargs)
  return converters.forecast_out(out, is_pandas)


def stl(x, s_window, **kwargs):
  '''
  Perform a decomposition of the time series x into seasonal, trend and 
  remainder components using loess. Most of the arguments listed below are 
  in **kwargs, and all of those arguments have sensible defaults. Usually 
  only the mandatory s_window paramter has to be set.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    s_window : either 'periodic' or the span (in lags) of the 
      loess window for seasonal extraction, which should be odd.
      This has no default.
    s_degree : Default 0, should be 0 or 1. Degree of local polynomial 
      for seasonal extraction.
    t_window : The span (in lags) of the loess window for trend extraction, 
      which should be odd. Default is a sensible, data-dependent value.
      See the R docs for the details.
    t_degree : Default 0, should be 0 or 1. Degree of local polynomial 
      for trend extraction.
    l_window : Span in lags of the loess window used to low-pass filter each 
      seasonal subseries. The default is first odd number greater than or 
      equal to frequency, which is recommmended.
    s_jump, t_jump, l_jump : integer parameters (min. 1) to increase speed of 
      each smoother by skipping data points.
    l_degree : Default is t.window, must be 0 or 1. Degree of local polynomial 
      for subseries low-pass filter.
    robust : Default is False. If True, robust loess fitting used.
    inner : number of backfitting iterations
    outer : number of outer robustness iterations
    na_action : Default is na.fail, which means that the user has to fill or 
      remove any missing values. If used, it must be an object that maps to 
      an R function, obtained from rpy2.
      
  Returns:
    If x is an R ts object, an R object of class 'stl' is returned. 
    If x is a Pandas Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  kwargs['s.window'] = s_window
  kwargs = converters.translate_kwargs(**kwargs)
  out = stats.stl(x, **kwargs)
  return converters.decomposition_out(out, is_pandas)


def decompose(x, type='additive'):
  '''
  Performs a classical seasonal decomposition of a time series into 
  season, trend and remainder components.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
      The series should be seasonal.
    type: Type of seasonal decomposition to perform.
      Default is 'additive', other option is 'multiplicative'.
      
  Returns:
    If x is an R ts object, an R object of class 'decomposed.ts' is returned. 
    If x is a Pandas Series, a Pandas Data Frame is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  out = stats.decompose(x, type=type)
  return converters.decomposition_out(out, is_pandas)

  
def seasadj(decomp):
  '''
  Return a seasonally adjusted version of the origin time series that 
  was seasonally decomposed to get decomp.
  
  Args:
    decomp: an R seasonal decomposition from stl or decompose
    
  Returns:
    an object that maps an R time series of the seasonally adjusted
    values of the series that decomp was formed from
  '''
  return fc.seasadj(decomp)


def sindexf(decomp, h):
  '''
  Projects the seasonal component of a seasonal decomposition of a time series 
  forward by h time steps into the future.
  
  Args:
    decomp: an R seasonal decomposition from stl or decompose
    h: a forecast horizon
    
  Returns:
    an object that maps to am R time series containing the seasonal component 
    of decomp, projected naively forward h steps.
  '''
  return fc.sindexf(x, h)
  

def BoxCox(x, lam):
  '''
  Applies a Box-Cox transformation to the data in x. This can stabilize the 
  variance of x, so that forecast model assumptions are more nearly satisfied.
  
  For x != 0, this is (x^lambda - 1) / lambda.
  For x = 0, it is log(x).
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    lam: BoxCox transformation parameter. 
      
  Returns:
    If x is an R ts object, an R time series is returned. 
    If x is a Pandas Series, a Pandas Series is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  out = fc.BoxCox(x, **{'lambda' : lam})
  return converters.series_out(out, is_pandas)
  

def InvBoxCox(x, lam):
  '''
  Invert a BoxCox transformation. The return value is a timeseries with 
  values of x transformed back to the original scale
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
      Its values that should be on the scale of a BoxCox transformation 
      with parameter lambda=lam.
    lam: BoxCox transformation parameter. 
      
  Returns:
    If x is an R ts object, an R time series is returned. 
    If x is a Pandas Series, a Pandas Series is returned.
  '''
  x, is_pandas = converters.to_ts(x)
  out = fc.InvBoxCox(x, **{'lambda' : lam})
  return converters.series_out(out, is_pandas)
  

def BoxCox_lambda(x, method='guerrero', lower=-1, upper=2):
  '''
  Function to find a good value of the BoxCox transformation parameter, lambda.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    method: Method of calculating lambda. 
      Default is 'guerrero', other option is 'lik' for log-likelihood.
    upper: Upper limit of possible lambda values, default 2.
    lower: Lower limit of possible lambda values, default -1.
    
  Returns:
    value of lambda for the series x, as calculated by the selected method
  '''
  x, _ = converters.to_ts(x)
  return fc.BoxCox_lambda(x, method=method, lower=lower, upper=upper)[0]


def na_interp(x, lam=NULL):
  '''
  Funtction for interpolating missing values in R time series. This function 
  uses linear interpolation for non-seasonal data. For seasonal data, it 
  uses an STL decomposition, imputing the seasonal value.
  
  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
      If lam is used, its values should be on the scale of a BoxCox
      transformation with parameter lambda=lam.
    lam: BoxCox transformation parameter. The default is R's NULL value.
      If NULL, no transformation is applied. Otherwise, a Box-Cox 
      transformation is applied before forecasting and inverted after.  
      
  Returns:
    If x is an R ts object, an R time series is returned. 
    If x is a Pandas Series, a Pandas Series is returned.
    In either case, missing values are filled.
  '''
  x, is_pandas = converters.to_ts(x)
  out = fc.na_interp(x, **{'lambda' : lam})
  return converters.series_out(out, is_pandas)
  

def accuracy(result, x=None, **kwargs):
  '''
  Computes an R matrix of forecast accuracy measures. Must take an R forecast 
  object for input, since the residuals are not included in the Pandas 
  output from forecast functions.  One step-ahead errors are computed over the 
  training data. Optionally, test data (x) can be included, in which case the 
  error measures are evaluated over the test set.
  
  The accuracy measures used are:
    * Mean Error (ME)
    * Root Mean Squared Error (RMSE)
    * Mean Absolute Error (MAE)
    * Mean Percentage Error (MPE)
    * Mean Absolute Percentage Error (MAPE)
    * Mean Absolute Scaled Error (MASE)
    * Autocorrelatino of Errors at Lag 1 (ACF1)
    * Theil's U (only if x provided)
  
  Args:
    result: an R forecast object
    x: optional R vector of true values for the forecast (test data)
    d: Number of first differences taken in forecast, default is none.
    D: Number of seasonal differences taken in forecast, default is none.

  Returns:
    An R list of forecast accuracy measures. 
    Use extractors.accuracy to get a Pandas DataFrame.  
  '''
  if x is not None:
    kwargs['x'] = x
  return fc.accuracy(result, **kwargs)


def tsclean(x, **kwargs):
  '''
  Identify and replace outliers. Uses loess for non-seasonal series and 
  an STL decomposition for seasonal series. Optionally fills missing values.

  Args:
    x: an R time series, obtained from converters.ts(), or a Pandas Series
      with the correct index (e.g. from converters.sequence_as_series().
    replace_missing: Default True. 
      If True, use na_interp to fill missing values in x.
    lam: optional BoxCox transformation parameter.
    
  Returns:
    If x is an R ts object, an R time series is returned. If x is a Pandas 
    Series, a Pandas Series is returned. In either case, outliers are replaced 
    and optionally, missing values are filled.
  '''
  x, is_pandas = converters.to_ts(x)
  kwargs = converters.translate_kwargs(**kwargs)
  out = fc.tsclean(x, **kwargs)
  return converters.series_out(out, is_pandas)


def findfrequency(x):
  '''
  Performs spectral analysis of x to find the dominant frequency, if there 
  is one.
  
  Args:
    x: an R time series or a Pandas Series

  Returns:
    The dominant frequency in x, or 1 if there isn't one.
  '''
  x, _ = converters.to_ts(x)
  return fc.findfrequency(x)[0]


def ndiffs(x, **kwargs):
  '''
  Estimates the number of first differences (non-seasonal) to take on the 
  time series, x, to reach stationarity.
  
  Args:
    x: an R time series or a Pandas Series
    alpha: Default 0.05, the level of the test used
    test : Test to use to determine number of first differences. Default 
        is 'kpss', for the KPSS test. Other values are 'adf' for augmented 
        Dickey-Fuller, or 'pp' for Phillips-Perron.
    max_d: max number of differences to try. Default is 2.
    
  Returns:
    The number of differences to take
  '''
  x, _ = converters.to_ts(x)
  kwargs = converters.translate_kwargs(**kwargs)
  return fc.ndiffs(x, **kwargs)[0]
  
  
def nsdiffs(x, **kwargs):
  '''
  Estimates the number of seasonal differences to take on the time series, 
  x, to reach stationarity. For this function, x must be a seasonal series.
  
  Args:
    x: an R time series or a Pandas Series
    m: Seasonal period. Default is frequency(x). No other value makes sense.
    test : Test to use to determine number of seasonal differences.
        Default is 'ocsb' for the Osborn-Chui-Smith-Birchenhall  test. 
        The alternative is 'ch' for the Canova-Hansen test. 
    max_D: Maximum number of seasonal differences to try. Default is 1.
    
  Returns:
    The number of seasonal differences to take
  '''
  x, _ = converters.to_ts(x)
  kwargs = converters.translate_kwargs(**kwargs)
  return fc.nsdiffs(x, **kwargs)[0]


def acf(x, lag_max=NULL):
  '''
  Function computes the autocorrelation of a univariate time series.
  
  Args:
    x: an R time series or a Pandas Series
    lag_max: The maximum number of lags to use. The default is NULL, which 
      uses a formula for the number of lags that should get a sensible value.

  Returns:
    The autocorrelation for all lags up to lag_max, either as a Pandas Series, 
    or as an R object.
  '''
  x, is_pandas = converters.to_ts(x)
  kwargs = {'lag.max' : lag_max}
  out = fc.Acf(x, plot=False, **kwargs)
  return converters.acf_out(out, is_pandas)
  
  
def pacf(x, lag_max=NULL):
  '''
  Function computes the partial autocorrelation of a univariate time series.
  
  Args:
    x: an R time series or a Pandas Series
    lag_max: The maximum number of lags to use. The default is NULL, which 
      uses a formula for the number of lags that should get a sensible value.

  Returns:
    The partial autocorrelation for all lags up to lag_max, either as a 
    Pandas Series, or as an R object.
  '''
  x, is_pandas = converters.to_ts(x)
  kwargs = {'lag.max' : lag_max}
  out = fc.Pacf(x, plot=False, **kwargs)
  return converters.acf_out(out, is_pandas)

















