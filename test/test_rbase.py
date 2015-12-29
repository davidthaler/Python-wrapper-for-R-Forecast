import unittest
from rpy2 import robjects
from rforecast import rbase, ts_io, converters, wrappers

class rbaseTestCase(unittest.TestCase):

  def setUp(self):
    self.oil = ts_io.read_series('data/oil.csv')
    self.oil_ts = converters.series_as_ts(self.oil)
    self.mat = converters.matrix([[1,2,3],[2,3,4]])
    self.acc = wrappers.accuracy(wrappers.thetaf(self.oil_ts))
    
  def testCls(self):
    self.assertTrue('ts' in rbase.cls(self.oil_ts))
    self.assertRaises(TypeError, rbase.cls, self.oil)
    
  def testDim(self):
    self.assertListEqual(rbase.dim(self.mat), [2, 3])
    self.assertTrue(rbase.dim(self.oil_ts) is None)    
    self.assertRaises(TypeError, rbase.dim, self.oil)
    
  def testColnames(self):
    self.assertRaises(TypeError, rbase.colnames, self.oil)
    self.assertTrue(rbase.colnames(self.mat) is None)
    self.assertTrue('MASE' in rbase.colnames(self.acc))


