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
    self.tsn = converters.ts([1, 2, NA, 4])
    self.tss = converters.ts([1, 2, 3, 1, 2, 3, 1, NA, 3], frequency=3)
    self.vss = [1,2,3,4] * 4
    self.vns = range(10)
    self.data = [0.74, 0.42, 0.22, 0.04, 0.17, 0.37, 
                 0.53, 0.32, 0.82, 0.81, 0.11, 0.79]
    self.npdata = numpy.array(self.data)
    
    
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


  def test_matrix_list(self):
    # wrappers.matrix turns a list into a column matrix
    mat = wrappers.matrix(self.data)
    self.assertTrue(type(mat) is robjects.Matrix)
    self.assertListEqual(list(mat), self.data)
    self.assertTrue(self._check_dim(mat, 12, 1))


  def test_matrix_array(self):
    data = numpy.array(self.data)
    mat = wrappers.matrix(data)
    self.assertTrue(type(mat) is robjects.Matrix)
    self.assertListEqual(list(mat), self.data)
    self.assertTrue(self._check_dim(mat, 12, 1))
    
    # test 2D numpy array
    data = data.reshape((4, 3))
    mat = wrappers.matrix(data)
    self.assertTrue(self._check_dim(mat, 4, 3))


  def test_matrix_series(self):
    # wrappers.matrix turns a Pandas Series into a column matrix
    s = pandas.Series(self.data)
    mat = wrappers.matrix(s)
    self.assertTrue(type(mat) is robjects.Matrix)
    self.assertListEqual(list(mat), self.data)
    self.assertTrue(self._check_dim(mat, 12, 1))


  def test_matrix_data_frame(self):
    data = self.npdata.reshape((4, 3))
    df = pandas.DataFrame(data)
    mat = wrappers.matrix(df)
    self.assertTrue(self._check_dim(mat, 4, 3))
    self.assertTrue( (numpy.array(mat) == df.values).all() )
    

  def _check_dim(self, mat, nrows, ncols):
    n = nrows * ncols
    r, c = robjects.r('dim')(mat)
    if len(mat) == n and r == nrows and c == ncols:
      return True
    else:
      return False




