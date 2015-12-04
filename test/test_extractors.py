import unittest
from rforecast import wrappers
from rforecast import extractors
import rpy2
import pandas
from rpy2 import robjects
from rpy2.robjects.packages import importr


class ExtractorsTestCase(unittest.TestCase):

  def setUp(self):
    self.fc = importr('forecast')
    importr('fpp')

    
    

    
    



  def test_mean_prediction(self):
    pred = converters.mean_prediction(self.fc_oil)
    self.assertAlmostEqual(pred[0], 370.3503, places=3)
    self.assertAlmostEqual(pred[-1], 370.3503, places=3)
    self.assertEqual(len(pred), 10)












