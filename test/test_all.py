import unittest
from rforecast import wrappers
from rforecast import converters
from rforecast import ts_io
from rpy2 import robjects
from rpy2.robjects.packages import importr


class EndToEndTestCase(unittest.TestCase):

  def setUp(self):
    self.oil_r  = ts_io.read_ts('oil', 'fpp', as_pandas=False)
    self.oil_py = converters.ts_as_series(self.oil_r)
    self.aus_r = ts_io.read_ts('austourists', 'fpp', as_pandas=False)
    self.aus_py = converters.ts_as_series(self.aus_r)
    self.austa_r = ts_io.read_ts('austa', 'fpp', as_pandas=False)
    self.austa_py = converters.ts_as_series(self.austa_r)
    self.fc = importr('forecast')

  def _check_points(self, fc_py, fc_r):
    '''
    Checks that the R and python forecasts are the same at select points
    for both the mean forecast and the prediction intervals. Compares the 
    first and last values of the mean forecast, and the first value of the 
    80% confidence lower PI and the last value of the 95% upper PI.
    
    Args:
      fc_py: the python forecast
      fc_r : the R forecast
      
    Return:
      Nothing, but makes tests assertions which can fail.
    '''
    lower = fc_r.rx2('lower')
    upper = fc_r.rx2('upper')
    mean  = fc_r.rx2('mean')
    self.assertAlmostEqual(fc_py.point_fc.iloc[0], mean[0], places=3)
    self.assertAlmostEqual(fc_py.point_fc.iloc[-1], mean[-1], places=3)
    self.assertAlmostEqual(fc_py.lower80.iloc[0], lower[0], places=3)
    self.assertAlmostEqual(fc_py.upper95.iloc[-1], upper[-1], places=3)
    
  def test_naive(self):
    fc_py = wrappers.naive(self.oil_py)
    fc_r  = self.fc.naive(self.oil_r)
    self._check_points(fc_py, fc_r)
    
  def test_thetaf(self):
    fc_py = wrappers.thetaf(self.oil_py)
    fc_r  = self.fc.thetaf(self.oil_r)
    self._check_points(fc_py, fc_r)
    
  def test_snaive(self):
    fc_py = wrappers.snaive(self.aus_py)
    fc_r  = self.fc.snaive(self.aus_r)
    self._check_points(fc_py, fc_r)
  
  def test_rwf(self):
    fc_py = wrappers.rwf(self.oil_py)
    fc_r  = self.fc.rwf(self.oil_r)
    self._check_points(fc_py, fc_r)

  def test_forecast_nonseasonal(self):
    fc_py = wrappers.forecast(self.oil_py)
    fc_r  = self.fc.forecast(self.oil_r)
    self._check_points(fc_py, fc_r)
    
  def test_forecast_seasonal(self):
    fc_py = wrappers.forecast(self.aus_py)
    fc_r  = self.fc.forecast(self.aus_r)
    self._check_points(fc_py, fc_r)
    
  def test_auto_arima_nonseasonal(self):
    fc_py = wrappers.auto_arima(self.oil_py)
    model = self.fc.auto_arima(self.oil_r)
    fc_r  = self.fc.forecast(model)
    self._check_points(fc_py, fc_r)

  def test_auto_arima_seasonal(self):
    fc_py = wrappers.auto_arima(self.aus_py)
    model = self.fc.auto_arima(self.aus_r)
    fc_r  = self.fc.forecast(model)
    self._check_points(fc_py, fc_r)

  def test_auto_arima_raises(self):
    self.assertRaises(ValueError, wrappers.auto_arima, self.oil_py , 
                       xreg=range(len(self.oil_py)))
    self.assertRaises(ValueError, wrappers.auto_arima, self.oil_py, h=10, 
                       newxreg=range(10))

  def test_stlf(self):
    fc_py = wrappers.stlf(self.aus_py)
    fc_r  = self.fc.stlf(self.aus_r)
    self._check_points(fc_py, fc_r)

  def test_acf(self):
    acf_py = wrappers.acf(self.oil_py, lag_max=10)
    self.assertEqual(acf_py.name, 'Acf')
    self.assertEqual(len(acf_py), 10)
    acf_r = self.fc.Acf(self.oil_r, plot=False, lag_max=10)
    self.assertAlmostEqual(acf_py[1], acf_r.rx2('acf')[1], places=3)
    self.assertAlmostEqual(acf_py[10], acf_r.rx2('acf')[10], places=3)

  def test_pacf(self):
    pacf_py = wrappers.pacf(self.oil_py, lag_max=10)
    self.assertEqual(pacf_py.name, 'Pacf')
    self.assertEqual(len(pacf_py), 10)
    pacf_r = self.fc.Pacf(self.oil_r, plot=False, **{'lag.max':10})
    self.assertAlmostEqual(pacf_py.values[0], pacf_r.rx2('acf')[0], places=3)
    self.assertAlmostEqual(pacf_py.values[-1], pacf_r.rx2('acf')[-1], places=3)

  def test_ses(self):
    fc_py = wrappers.ses(self.oil_py)
    fc_r  = self.fc.ses(self.oil_r, initial='simple')
    self._check_points(fc_py, fc_r)

  def test_ses_raises(self):
    self.assertRaises(ValueError, wrappers.ses, self.oil_py, alpha=0)
    self.assertRaises(ValueError, wrappers.ses, self.oil_py, alpha=1.0)

  def test_holt(self):
    fc_py = wrappers.holt(self.austa_py)
    fc_r  = self.fc.holt(self.austa_r, initial='simple')
    self._check_points(fc_py, fc_r)
    
  def test_holt_raises(self):
    self.assertRaises(ValueError, wrappers.holt, self.austa_py, alpha=0)
    self.assertRaises(ValueError, wrappers.holt, self.austa_py, alpha=1.0)
    self.assertRaises(ValueError, wrappers.holt, self.austa_py, beta=0)
    self.assertRaises(ValueError, wrappers.holt, self.austa_py, beta=1.0)

  def test_hw(self):
    fc_py = wrappers.hw(self.aus_py)
    fc_r  = self.fc.hw(self.aus_r, initial='simple')
    self._check_points(fc_py, fc_r)

  def test_hw_raises(self):
    self.assertRaises(ValueError, wrappers.hw, self.aus_py, alpha=0)
    self.assertRaises(ValueError, wrappers.hw, self.aus_py, alpha=1.0)
    self.assertRaises(ValueError, wrappers.hw, self.aus_py, beta=0)
    self.assertRaises(ValueError, wrappers.hw, self.aus_py, beta=1.0)
    self.assertRaises(ValueError, wrappers.hw, self.aus_py, gamma=0)
    self.assertRaises(ValueError, wrappers.hw, self.aus_py, gamma=1.0)
    
  def test_arima_seasonal(self):
    fc_py = wrappers.arima(self.aus_py, order=(1,0,0), seasonal=(1,1,0), 
                        include_constant=True)
    order = robjects.r.c(1., 0., 0.)
    seasonal = robjects.r.c(1., 1., 0.)
    model = self.fc.Arima(self.aus_r, order=order, seasonal=seasonal, 
                        include_constant=True)
    fc_r = self.fc.forecast(model)
    self._check_points(fc_py, fc_r)
    self.assertEqual(fc_py.shape[0], 8)
    
  def test_arima_nonseasonal(self):
    fc_py = wrappers.arima(self.oil_py, order=(0,1,0))
    order = robjects.r.c(0., 1., 0.)
    model = self.fc.Arima(self.oil_r, order=order)
    fc_r  = self.fc.forecast(model)
    self._check_points(fc_py, fc_r)
    self.assertEqual(fc_py.shape[0], 10)






