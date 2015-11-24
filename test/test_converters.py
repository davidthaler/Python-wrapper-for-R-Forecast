import unittest
from rforecast import converters
from rforecast import extractors
from rforecast import wrappers
from rpy2 import robjects
from rpy2.robjects.packages import importr
import pandas


class ConvertersTestCase(unittest.TestCase):

  def setUp(self):
    importr('fpp')
    self.oil = list(robjects.r('oil'))
    self.aus = list(robjects.r('austourists'))


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




