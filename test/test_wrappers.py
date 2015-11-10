import unittest
from rforecast import wrappers
import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr

NULL = robjects.NULL
NA = robjects.NA_Real


class WrappersTestCase(unittest.TestCase):


  def setUp(self):
    self.fc = importr('forecast')
    importr('fpp')
    self.oil = robjects.r('oil')
    self.aus = robjects.r('austourists')
    self.tsn = wrappers.ts([1, 2, NA, 4])
    self.tss = wrappers.ts([1, 2, 3, 1, 2, 3, 1, NA, 3], frequency=3)
    self.vss = [1,2,3,4] * 4
    self.vns = range(10)
    
    
  def test_frequency(self):
    self.assertEqual(wrappers.frequency(self.oil), 1)
    self.assertEqual(wrappers.frequency(self.aus), 4)

    
  def test_map_args(self):
    self.assertEqual(wrappers._map_arg(3), 3)
    arg = wrappers._map_arg((1, 2))
    self.assertEqual(list(arg), [1, 2])
    self.assertEqual(type(arg), rpy2.robjects.vectors.IntVector)

    
  def test_translate_kwargs(self):
    self.assertEquals(wrappers._translate_kwargs(lam=1), {'lambda' : 1})
    arg = wrappers._translate_kwargs(levels=(80, 95))
    self.assertEquals(type(arg['levels']), rpy2.robjects.vectors.IntVector)
    self.assertEquals(list(arg['levels']), [80, 95])
    arg = wrappers._translate_kwargs(s_window=7)
    self.assertEquals(arg, {'s.window' : 7})


  def test_na_interp(self):
    self.assertEquals(list(wrappers.na_interp(self.tsn)), [1, 2, 3, 4])
    seasonal = list(wrappers.na_interp(self.tss))
    self.assertAlmostEqual(seasonal[7], 2.0, places=3)


  def test_ts(self):
    ts = wrappers.ts(self.vss, deltat=0.25, end=(1,1))
    self.assertEqual(wrappers.frequency(ts), 4)
    self.assertEqual(tuple(robjects.r('end')(ts)), (1.0, 1.0))
    self.assertEqual(tuple(robjects.r('start')(ts)), (-3.0, 2.0))


  def test_get_horizon(self):
    self.assertEqual(wrappers._get_horizon(self.aus), 8)
    self.assertEqual(wrappers._get_horizon(self.aus, 10), 10)
    self.assertEqual(wrappers._get_horizon(self.oil), 10)


