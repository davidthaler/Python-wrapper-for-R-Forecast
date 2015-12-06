import unittest
import pandas
from rforecast import ts_io

class IOTestCase(unittest.TestCase):

  def test_read_series(self):
    # The no-index case:
    oil2 = ts_io.read_series('data/oil2.csv')
    self.assertEqual(len(oil2), 46)
    self.assertListEqual(list(oil2.index), range(1, 46 + 1))
    
    # The non-seasonal index case:
    oil = ts_io.read_series('data/oil.csv')
    self.assertEqual(len(oil), 46)
    self.assertListEqual(list(oil.index), range(1965, 2011))
    
    # The seasonal index case:
    aus = ts_io.read_series('data/aus.csv')
    self.assertEqual(len(aus), 48)
    self.assertEqual(aus.index.nlevels, 2)

    # This has 4 columns, and should raise an IOError:
    self.assertRaises(IOError, ts_io.read_series, 'data/bad.csv')

