import unittest
from rforecast import wrappers
from rforecast import converters
from rpy2 import robjects
from rpy2.robjects.packages import importr
import pandas
import numpy


class ConvertersTestCase(unittest.TestCase):

  def setUp(self):
    importr('fpp')
    self.oil_ts = robjects.r('oil')
    self.aus_ts = robjects.r('austourists')
    self.fc_oil = wrappers.meanf(self.oil_ts)
    self.fc_aus = wrappers.ets(self.aus_ts)
    self.oil = list(robjects.r('oil'))
    self.aus = list(robjects.r('austourists'))
    self.data = [0.74, 0.42, 0.22, 0.04, 0.17, 0.37, 
                 0.53, 0.32, 0.82, 0.81, 0.11, 0.79]
    self.npdata = numpy.array(self.data)


  def test_translate_kwargs(self):
    self.assertEquals(converters.translate_kwargs(lam=1), {'lambda' : 1})
    arg = converters.translate_kwargs(levels=(80, 95))
    self.assertEquals(type(arg['levels']), robjects.vectors.IntVector)
    self.assertEquals(list(arg['levels']), [80, 95])
    arg = converters.translate_kwargs(s_window=7)
    self.assertEquals(arg, {'s.window' : 7})

    
  def test_map_arg(self):
    self.assertEqual(converters.map_arg(3), 3)
    arg = converters.map_arg((1, 2))
    self.assertEqual(list(arg), [1, 2])
    self.assertEqual(type(arg), robjects.vectors.IntVector)
    
    
  def test_sequence_as_series(self):
    oil = converters.sequence_as_series(self.oil, start=1965)
    aus = converters.sequence_as_series(self.aus, start=(1999, 1), freq=4)
    self.assertEqual(oil.shape, (46,))
    self.assertEqual(oil.index.nlevels, 1)
    self.assertEqual(oil.index[0], 1965)
    self.assertEqual(oil.index[-1], 2010)
    self.assertAlmostEqual(oil[1965], 111.00, places=1)
    self.assertAlmostEqual(oil[2010], 467.77, places=1)
    
    self.assertEqual(aus.shape, (48, ))
    self.assertEqual(aus.index.nlevels, 2)
    self.assertEqual(aus.index[0], (1999, 1))
    self.assertEqual(aus.index[-1], (2010, 4))
    self.assertEqual(aus[2010].shape, (4,))
    self.assertAlmostEqual(aus[(1999, 1)], 30.05, places=1)
    self.assertAlmostEqual(aus[(2010, 4)], 47.91, places=1)

    aus2 = converters.sequence_as_series(self.aus, start=1999, freq=4)
    self.assertTrue(aus2.equals(aus))
    
        
  def test_series_as_ts(self):
    oil = converters.sequence_as_series(self.oil, start=1965)
    oil_ts = converters.series_as_ts(oil)
    self.assertTrue(type(oil_ts) is robjects.FloatVector)
    tsp = robjects.r('tsp')(oil_ts)
    self.assertAlmostEqual(tsp[0], 1965, places=1)
    self.assertAlmostEqual(tsp[1], 2010, places=1)
    self.assertAlmostEqual(tsp[2], 1, places=1)

    aus = converters.sequence_as_series(self.aus, start=(1999, 1), freq=4)
    aus_ts = converters.series_as_ts(aus)
    self.assertTrue(type(aus_ts) is robjects.FloatVector)
    tsp = robjects.r('tsp')(aus_ts)
    self.assertAlmostEqual(tsp[0], 1999, places=2)
    self.assertAlmostEqual(tsp[1], 2010.75, places=2)
    self.assertAlmostEqual(tsp[2], 4, places=1)


# Function matrix moved in from wrappers.py


  def test_matrix_list(self):
    # converters.matrix turns a list into a column matrix
    mat = converters.matrix(self.data)
    self.assertTrue(type(mat) is robjects.Matrix)
    self.assertListEqual(list(mat), self.data)
    self.assertTrue(self._check_dim(mat, 12, 1))


  def test_matrix_array(self):
    data = numpy.array(self.data)
    mat = converters.matrix(data)
    self.assertTrue(type(mat) is robjects.Matrix)
    self.assertListEqual(list(mat), self.data)
    self.assertTrue(self._check_dim(mat, 12, 1))
    
    # test 2D numpy array
    data = data.reshape((4, 3))
    mat = converters.matrix(data)
    self.assertTrue(self._check_dim(mat, 4, 3))


  def test_matrix_series(self):
    # converters.matrix turns a Pandas Series into a column matrix
    s = pandas.Series(self.data)
    mat = converters.matrix(s)
    self.assertTrue(type(mat) is robjects.Matrix)
    self.assertListEqual(list(mat), self.data)
    self.assertTrue(self._check_dim(mat, 12, 1))


  def test_matrix_data_frame(self):
    data = self.npdata.reshape((4, 3))
    df = pandas.DataFrame(data)
    mat = converters.matrix(df)
    self.assertTrue(self._check_dim(mat, 4, 3))
    self.assertTrue( (numpy.array(mat) == df.values).all() )
    

  def _check_dim(self, mat, nrows, ncols):
    n = nrows * ncols
    r, c = robjects.r('dim')(mat)
    if len(mat) == n and r == nrows and c == ncols:
      return True
    else:
      return False


# Functions moved in from extractors.py

  def test_get_index(self):
    oil_idx = converters._get_index(self.oil_ts)
    self.assertEqual(oil_idx, range(1965, 2011))
    aus_idx = converters._get_index(self.aus_ts)
    self.assertEqual(len(aus_idx), 2)
    self.assertEqual(len(aus_idx[0]), 48)
    self.assertEqual(len(aus_idx[1]), 48)
    self.assertEqual(aus_idx[1], [1,2,3,4] * 12)


  def test_ts_as_series(self):
    oil = converters.ts_as_series(self.oil_ts)
    self.assertEqual(list(oil.index), range(1965, 2011))
    self.assertAlmostEqual(oil[1965], 111.0091, places=3)
    self.assertAlmostEqual(oil[2010], 467.7724, places=3)
    aus = converters.ts_as_series(self.aus_ts)
    self.assertAlmostEqual(aus[(1999, 1)], 30.0525, places=3)
    self.assertAlmostEqual(aus[(2010, 4)], 47.9137, places=3)
    self.assertEqual(aus[2010].shape, (4, ))
    self.assertEqual(type(aus.index), pandas.core.index.MultiIndex)
    self.assertEqual(aus.index[0], (1999, 1))
    self.assertEqual(aus.index[-1], (2010, 4))


  def test_decomposition(self):
    dc = wrappers.stl(self.aus_ts, 7)
    dcdf = converters.decomposition(dc)
    self.assertEqual(type(dcdf.index), pandas.core.index.MultiIndex)
    self.assertEqual(dcdf.index[0], (1999, 1))
    self.assertEqual(dcdf.index[-1], (2010, 4))
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
    
    dc = wrappers.decompose(self.aus_ts)
    dcdf = converters.decomposition(dc)
    self.assertEqual(type(dcdf.index), pandas.core.index.MultiIndex)
    self.assertEqual(dcdf.index[0], (1999, 1))
    self.assertEqual(dcdf.index[-1], (2010, 4))
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
    self.assertRaises(ValueError, converters.decomposition, self.fc_oil)


  def test_prediction_intervals(self):
    pred = converters.prediction_intervals(self.fc_oil)
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
    self.assertRaises(ValueError, converters.prediction_intervals, self.oil_ts)


  def test_accuracy(self):
    acc1 = wrappers.accuracy(self.fc_oil)
    acdf1 = converters.accuracy(acc1)
    acdf1.shape == (7, 1)
    list(acdf1.columns) == ['Train']
    acc2 = wrappers.accuracy(self.fc_oil, 350)
    acdf2 = converters.accuracy(acc2)
    acdf2.shape == (7, 2)
    set(acdf2.columns) == {'Train', 'Test'}
    self.assertTrue(acdf1.Train.round(5).equals(acdf2.Train.round(5)))
    self.assertAlmostEqual(acdf2.Test.ix['ME'], -20.3502, places=3)
    self.assertAlmostEqual(acdf2.Test.ix['MAE'], 20.3502, places=3)
    self.assertAlmostEqual(acdf2.Test.ix['RMSE'], 20.3502, places=3)








