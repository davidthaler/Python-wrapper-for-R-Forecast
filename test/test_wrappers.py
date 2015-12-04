import unittest
from rforecast import wrappers
from rforecast import converters
import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr
import numpy
import pandas


NULL = robjects.NULL
NA = robjects.NA_Real


class WrappersTestCase(unittest.TestCase):


  def setUp(self):
    self.fc = importr('forecast')
    importr('fpp')
    self.oil = robjects.r('oil')
    self.aus = robjects.r('austourists')
    self.gold = robjects.r('gold')
    self.tsn = converters.ts([1, 2, NA, 4])
    self.tss = converters.ts([1, 2, 3, 1, 2, 3, 1, NA, 3], frequency=3)
    self.vss = [1,2,3,4] * 4
    self.vns = range(10)
    
    
  def test_frequency(self):
    self.assertEqual(wrappers.frequency(self.oil), 1)
    self.assertEqual(wrappers.frequency(self.aus), 4)


  def test_na_interp(self):
    self.assertEquals(list(wrappers.na_interp(self.tsn)), [1, 2, 3, 4])
    seasonal = list(wrappers.na_interp(self.tss))
    self.assertAlmostEqual(seasonal[7], 2.0, places=3)


  def test_ts(self):
    ts = converters.ts(self.vss, deltat=0.25, end=(1,1))
    self.assertEqual(wrappers.frequency(ts), 4)
    self.assertEqual(tuple(robjects.r('end')(ts)), (1.0, 1.0))
    self.assertEqual(tuple(robjects.r('start')(ts)), (-3.0, 2.0))


  def test_get_horizon(self):
    self.assertEqual(wrappers._get_horizon(self.aus), 8)
    self.assertEqual(wrappers._get_horizon(self.aus, 10), 10)
    self.assertEqual(wrappers._get_horizon(self.oil), 10)


  def test_box_cox(self):
    bc = wrappers.BoxCox(self.oil, 0.5)
    bc1 = wrappers.BoxCox(self.oil, 1)
    bc0 = wrappers.BoxCox(self.oil, 0)
    self.assertAlmostEqual(self.oil[0], bc1[0] + 1, places=4)
    self.assertAlmostEqual(numpy.log(self.oil[0]), bc0[0], places=4)
    self.assertAlmostEqual(bc[0], 19.07217, places=4)
    inv_bc = wrappers.InvBoxCox(bc, 0.5)
    self.assertAlmostEqual(inv_bc[0], self.oil[0], places=4)

  def test_tsclean(self):
    clean_gold = wrappers.tsclean(converters.ts_as_series(self.gold))
    self.assertFalse(clean_gold.isnull().any())
    self.assertAlmostEqual(clean_gold[56], 309.875, places=3)
    self.assertAlmostEqual(clean_gold[419], 373.975, places=3)
    self.assertAlmostEqual(clean_gold[604], 459.175, places=3)







