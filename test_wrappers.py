import unittest
import wrappers
import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr

class WrappersTestCase(unittest.TestCase):


  def setUp(self):
    self.fc = importr('forecast')
    importr('fpp')
    self.oil = robjects.r('oil')
    self.aus = robjects.r('austourists')
    
    
  def testFrequency(self):
    self.assertEqual(wrappers.frequency(self.oil), 1)
    self.assertEqual(wrappers.frequency(self.aus), 4)

    
  def testMapArgs(self):
    self.assertEqual(wrappers._map_arg(3), 3)
    arg = wrappers._map_arg((1, 2))
    self.assertEqual(list(arg), [1, 2])
    self.assertEqual(type(arg), rpy2.robjects.vectors.IntVector)

    
  def testTranslateKwargs(self):
    self.assertEquals(wrappers._translate_kwargs(lam=1), {'lambda' : 1})
    arg = wrappers._translate_kwargs(levels=(80, 95))
    self.assertEquals(type(arg['levels']), rpy2.robjects.vectors.IntVector)
    self.assertEquals(list(arg['levels']), [80, 95])
    arg = wrappers._translate_kwargs(s_window=7)
    self.assertEquals(arg, {'s.window' : 7})






