import unittest
from rforecast import wrappers
from rforecast import io


class EndToEndTestCase(unittest.TestCase):

  def setUp(self):
    self.oil = io.read_ts('data/oil.csv')
    self.aus = io.read_ts('data/aus.csv')

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


