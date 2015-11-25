import unittest
import pandas
from rforecast import io

class IOTestCase(unittest.TestCase):

  def test_read_ts(self):
    # The no-index case:
    oil2 = io.read_ts('data/oil2.csv')
    self.assertEqual(len(oil2), 46)
    self.assertListEqual(list(oil2.index), range(1, 46 + 1))
    
    # The non-seasonal index case:
    oil = io.read_ts('data/oil.csv')
    self.assertEqual(len(oil), 46)
    self.assertListEqual(list(oil.index), range(1965, 2011))
    
    # The seasonal index case:
    aus = io.read_ts('data/aus.csv')
    self.assertEqual(len(aus), 48)
    self.assertEqual(aus.index.nlevels, 2)

    # This has 4 columns, and should raise an IOError:
    self.assertRaises(IOError, io.read_ts, 'data/bad.csv')
    
    
    