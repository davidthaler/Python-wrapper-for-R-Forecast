import unittest
from rforecast import wrappers
from rforecast import ts_io


class EndToEndTestCase(unittest.TestCase):

  def setUp(self):
    self.oil = ts_io.read_series('data/oil.csv')
    self.aus = ts_io.read_series('data/aus.csv')
    self.austa = ts_io.read_ts('austa', 'fpp')

  def test_naive(self):
    fc = wrappers.naive(self.oil)
    self.assertAlmostEqual(fc.point_fc[2011], 467.7724, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 467.7724, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 404.6370, places=3)
    self.assertAlmostEqual(fc.upper95[2020], 773.1130, places=3)
    
  def test_thetaf(self):
    fc = wrappers.thetaf(self.oil)
    self.assertAlmostEqual(fc.point_fc[2011], 470.9975, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 500.0231, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 408.5509, places=3)
    self.assertAlmostEqual(fc.upper95[2020], 802.0053, places=3)
    
  def test_snaive(self):
    fc = wrappers.snaive(self.aus)
    self.assertAlmostEqual(fc.point_fc[(2011, 1)], 59.76678, places=3)
    self.assertAlmostEqual(fc.point_fc[(2012, 4)], 47.91374, places=3)
    self.assertAlmostEqual(fc.lower80[(2011, 1)], 55.37882, places=3)
    self.assertAlmostEqual(fc.upper95[(2012, 4)], 57.40424, places=3)
  
  def test_rwf(self):
    fc = wrappers.rwf(self.oil)
    self.assertAlmostEqual(fc.point_fc[2011], 467.7724, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 467.7724, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 404.7558, places=3)
    self.assertAlmostEqual(fc.upper95[2020], 772.5385, places=3)

  def test_forecast_ts(self):
    fc = wrappers.forecast_ts(self.oil)
    self.assertAlmostEqual(fc.point_fc[2011], 467.7721, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 467.7721, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 405.3255, places=3)
    self.assertAlmostEqual(fc.upper95[2020], 769.7543, places=3)
    fc = wrappers.forecast_ts(self.aus)
    self.assertAlmostEqual(fc.point_fc[(2011, 1)], 57.87294, places=3)
    self.assertAlmostEqual(fc.point_fc[(2012, 4)], 52.84327, places=3)
    self.assertAlmostEqual(fc.lower80[(2011, 1)], 53.30794, places=3)
    self.assertAlmostEqual(fc.upper95[(2012, 4)], 62.60852, places=3)
    
  def test_auto_arima(self):
    fc = wrappers.auto_arima(self.oil)
    self.assertAlmostEqual(fc.point_fc[2011], 475.7004, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 547.0531, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 412.6839, places=3)
    self.assertAlmostEqual(fc.upper95[2020], 851.8193, places=3)
    fc = wrappers.auto_arima(self.aus)
    self.assertAlmostEqual(fc.point_fc[(2011, 1)], 60.64208, places=3)
    self.assertAlmostEqual(fc.point_fc[(2012, 4)], 51.55356, places=3)
    self.assertAlmostEqual(fc.lower80[(2011, 1)], 57.57010, places=3)
    self.assertAlmostEqual(fc.upper95[(2012, 4)], 57.52426, places=3)

  def test_stlf(self):
    fc = wrappers.stlf(self.aus)    
    self.assertAlmostEqual(fc.point_fc[(2011, 1)], 58.88951, places=3)
    self.assertAlmostEqual(fc.point_fc[(2012, 4)], 51.68499, places=3)
    self.assertAlmostEqual(fc.lower80[(2011, 1)], 56.69656, places=3)
    self.assertAlmostEqual(fc.upper95[(2012, 4)], 57.59713, places=3)

  def test_acf(self):
    acf = wrappers.acf(self.oil, lag_max=10)
    self.assertEqual(acf.name, 'Acf')
    self.assertEqual(len(acf), 10)
    self.assertAlmostEqual(acf[1], 0.8708, places=3)
    self.assertAlmostEqual(acf[10], -0.2016, places=3)

  def test_pacf(self):
    acf = wrappers.pacf(self.oil, lag_max=10)
    self.assertEqual(acf.name, 'Pacf')
    self.assertEqual(len(acf), 10)
    self.assertAlmostEqual(acf[1], 0.8708, places=3)
    self.assertAlmostEqual(acf[10], 0.1104, places=3)

  def test_ses(self):
    fc = wrappers.ses(self.oil, level=80)
    self.assertAlmostEqual(fc.point_fc[2011], 467.7724, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 467.7724, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 405.3270, places=3)
    self.assertAlmostEqual(fc.upper80[2020], 665.2418, places=3)
    self.assertRaises(ValueError, wrappers.ses, self.oil, alpha=0)
    self.assertRaises(ValueError, wrappers.ses, self.oil, alpha=1.0)

  def test_holt(self):
    fc = wrappers.holt(self.austa, damped=True)
    self.assertAlmostEqual(fc.point_fc[2011], 5.5503, places=3)
    self.assertAlmostEqual(fc.point_fc[2020], 6.4417, places=3)
    self.assertAlmostEqual(fc.lower80[2011], 5.3209, places=3)
    self.assertAlmostEqual(fc.upper95[2020], 7.7942, places=3)
    self.assertRaises(ValueError, wrappers.holt, self.austa, alpha=0)
    self.assertRaises(ValueError, wrappers.holt, self.austa, alpha=1.0)
    self.assertRaises(ValueError, wrappers.holt, self.austa, beta=0)
    self.assertRaises(ValueError, wrappers.holt, self.austa, beta=1.0)

  def test_hw(self):
    fc = wrappers.hw(self.aus)
    self.assertAlmostEqual(fc.point_fc[(2011, 1)], 60.0507, places=3)
    self.assertAlmostEqual(fc.point_fc[(2012, 4)], 52.2922, places=3)
    self.assertAlmostEqual(fc.lower80[(2011, 1)], 56.9353, places=3)
    self.assertAlmostEqual(fc.upper95[(2012, 4)], 64.7920, places=3)
    self.assertRaises(ValueError, wrappers.hw, self.aus, alpha=0)
    self.assertRaises(ValueError, wrappers.hw, self.aus, alpha=1.0)
    self.assertRaises(ValueError, wrappers.hw, self.aus, beta=0)
    self.assertRaises(ValueError, wrappers.hw, self.aus, beta=1.0)
    self.assertRaises(ValueError, wrappers.hw, self.aus, gamma=0)
    self.assertRaises(ValueError, wrappers.hw, self.aus, gamma=1.0)

  def test_arima(self):
    fc = wrappers.arima(self.aus, order=(1,0,0), seasonal=(1,1,0), 
                        include_constant=True)
    self.assertAlmostEqual(fc.point_fc[(2011, 1)], 60.6420, places=3)
    self.assertAlmostEqual(fc.point_fc[(2012, 4)], 51.5535, places=3)
    self.assertAlmostEqual(fc.lower80[(2011, 1)], 57.5701, places=3)
    self.assertAlmostEqual(fc.upper95[(2012, 4)], 57.5242, places=3)
    self.assertEqual(fc.shape[0], 8)
    fc = wrappers.arima(self.oil, order=(0,1,0))
    self.assertEqual(fc.shape[0], 10)






