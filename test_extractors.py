import unittest
import wrappers
import extractors
import rpy2
import pandas
from rpy2 import robjects
from rpy2.robjects.packages import importr


class ExtractorsTestCase(unittest.TestCase):

  def setUp(self):
    self.fc = importr('forecast')
    importr('fpp')
    self.oil = robjects.r('oil')
    self.aus = robjects.r('austourists')
    self.fc_oil = wrappers.meanf(self.oil)
    self.fc_aus = wrappers.ets(self.aus)
    
    
  def test_get_index(self):
    oil_idx = extractors._get_index(self.oil)
    self.assertEqual(oil_idx, range(1965, 2011))
    aus_idx = extractors._get_index(self.aus)
    self.assertEqual(len(aus_idx), 2)
    self.assertEqual(len(aus_idx[0]), 48)
    self.assertEqual(len(aus_idx[1]), 48)
    self.assertEqual(aus_idx[1], [1,2,3,4] * 12)
    
    
  def test_ts_as_series(self):
    oil = extractors.ts_as_series(self.oil)
    self.assertEqual(list(oil.index), range(1965, 2011))
    self.assertAlmostEqual(oil[1965], 111.0091, places=3)
    self.assertAlmostEqual(oil[2010], 467.7724, places=3)
    aus = extractors.ts_as_series(self.aus)
    self.assertAlmostEqual(aus[(1999, 1)], 30.0525, places=3)
    self.assertAlmostEqual(aus[(2010, 4)], 47.9137, places=3)
    self.assertEquals(aus[2010].shape, (4, ))
    self.assertEquals(type(aus.index), pandas.core.index.MultiIndex)
    self.assertEquals(aus.index[0], (1999, 1))
    self.assertEquals(aus.index[-1], (2010, 4))


  def test_mean_prediction(self):
    pred = extractors.mean_prediction(self.fc_oil)
    self.assertAlmostEqual(pred[0], 370.3503, places=3)
    self.assertAlmostEqual(pred[-1], 370.3503, places=3)
    self.assertEqual(len(pred), 10)


  def test_decomposition(self):
    dc = wrappers.stl(self.aus, 7)
    dcdf = extractors.decomposition(dc)
    self.assertEquals(type(dcdf.index), pandas.core.index.MultiIndex)
    self.assertEquals(dcdf.index[0], (1999, 1))
    self.assertEquals(dcdf.index[-1], (2010, 4))
    self.assertEqual(dcdf.shape, (48, 4))
    self.assertEqual(list(dcdf.columns), [u'data', u'seasonal', u'trend', u'remainder'])
    self.assertAlmostEqual(dcdf.data[(1999, 1)], 30.0525, places=3)
    self.assertAlmostEqual(dcdf.data[(2010, 4)], 47.9137, places=3)
    self.assertAlmostEqual(dcdf.seasonal[(1999, 1)], 5.5077, places=3)
    self.assertAlmostEqual(dcdf.seasonal[(2010, 4)], 0.7848, places=3)
    self.assertAlmostEqual(dcdf.trend[(1999, 1)], 24.3714, places=3)
    self.assertAlmostEqual(dcdf.trend[(2010, 4)], 47.1525, places=3)
    self.assertAlmostEqual(dcdf.remainder[(1999, 1)], 0.1732, places=3)
    self.assertAlmostEqual(dcdf.remainder[(2010, 4)], -0.0236, places=3)
    
    dc = wrappers.decompose(self.aus)
    dcdf = extractors.decomposition(dc)
    self.assertEquals(type(dcdf.index), pandas.core.index.MultiIndex)
    self.assertEquals(dcdf.index[0], (1999, 1))
    self.assertEquals(dcdf.index[-1], (2010, 4))
    self.assertEqual(dcdf.shape, (48, 4))
    self.assertEqual(list(dcdf.columns), [u'data', u'seasonal', u'trend', u'remainder'])
    self.assertAlmostEqual(dcdf.data[(1999, 1)], 30.0525, places=3)
    self.assertAlmostEqual(dcdf.data[(2010, 4)], 47.9137, places=3)
    self.assertAlmostEqual(dcdf.seasonal[(1999, 1)], 8.5906, places=3)
    self.assertAlmostEqual(dcdf.seasonal[(2010, 4)], 1.5042, places=3)
    self.assertAlmostEqual(dcdf.trend[(1999, 3)], 25.7805, places=3)
    self.assertAlmostEqual(dcdf.trend[(2010, 2)], 46.514102, places=3)
    self.assertTrue(dcdf.trend.isnull()[(1999, 1)])
    self.assertTrue(dcdf.trend.isnull()[(1999, 2)])
    self.assertTrue(dcdf.trend.isnull()[(2010, 3)])
    self.assertTrue(dcdf.trend.isnull()[(2010, 4)])
    self.assertAlmostEqual(dcdf.remainder[(1999, 3)], 1.3091, places=3)
    self.assertAlmostEqual(dcdf.remainder[(2010, 2)], -2.9993, places=3)
    self.assertTrue(dcdf.remainder.isnull()[(1999, 1)])
    self.assertTrue(dcdf.remainder.isnull()[(1999, 2)])
    self.assertTrue(dcdf.remainder.isnull()[(2010, 3)])
    self.assertTrue(dcdf.remainder.isnull()[(2010, 4)])
    self.assertRaises(ValueError, extractors.decomposition, self.fc_oil)


  def test_prediction_intervals(self):
    pred = extractors.prediction_intervals(self.fc_oil)
    self.assertEqual(pred.shape, (10, 5))
    self.assertEqual(list(pred.index), range(2011, 2021))
    self.assertEqual(list(pred.columns), [u'point_fc', u'lower80', 
                    u'upper80', u'lower95', u'upper95'])
    self.assertAlmostEqual(pred.point_fc[2011], 370.3502, places=3)
    self.assertAlmostEqual(pred.point_fc[2020], 370.3502, places=3)
    self.assertAlmostEqual(pred.lower80[2011], 204.1084, places=3)
    self.assertAlmostEqual(pred.lower80[2020], 204.1084, places=3)
    self.assertAlmostEqual(pred.upper80[2011], 536.5920, places=3)
    self.assertAlmostEqual(pred.upper80[2020], 536.5920, places=3)
    self.assertAlmostEqual(pred.lower95[2011], 112.9187, places=3)
    self.assertAlmostEqual(pred.lower95[2020], 112.9187, places=3)
    self.assertAlmostEqual(pred.upper95[2011], 627.7818, places=3)
    self.assertAlmostEqual(pred.upper95[2020], 627.7818, places=3)
    self.assertRaises(ValueError, extractors.prediction_intervals, self.oil)


  def test_accuracy(self):
    acc1 = wrappers.accuracy(self.fc_oil)
    acdf1 = extractors.accuracy(acc1)
    acdf1.shape == (7, 1)
    list(acdf1.columns) == ['Train']
    acc2 = wrappers.accuracy(self.fc_oil, 350)
    acdf2 = extractors.accuracy(acc2)
    acdf2.shape == (7, 2)
    set(acdf2.columns) == {'Train', 'Test'}
    self.assertTrue(acdf1.Train.round(5).equals(acdf2.Train.round(5)))
    self.assertAlmostEqual(acdf2.Test.ix['ME'], -20.3502, places=3)
    self.assertAlmostEqual(acdf2.Test.ix['MAE'], 20.3502, places=3)
    self.assertAlmostEqual(acdf2.Test.ix['RMSE'], 20.3502, places=3)







