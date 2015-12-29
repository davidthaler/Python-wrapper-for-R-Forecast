from rpy2 import robjects
from rbase import cls, dim, colnames
import pandas
    
def is_R_forecast(fc):
  return type(fc) is robjects.ListVector and 'forecast' in cls(fc)
  
def is_Pandas_forecast(fc):
  return type(fc) is pandas.DataFrame and 'point_fc' in fc.columns

def is_forecast(fc):
  return is_R_forecast(fc) or is_Pandas_forecast(fc)

def is_R_decomposition(dc):
  return (type(dc) is robjects.ListVector 
          and cls(dc)[0] in ['stl', 'decomposed.ts'])
          
def is_Pandas_decomposition(dc):
  col_names = [u'data', u'seasonal', u'trend', u'remainder']
  return (type(dc) is pandas.DataFrame and dc.shape[1] == 4 
          and len(set(dc.columns).intersection(col_names)) == 4)

def is_decomposition(dc):
  return is_Pandas_decomposition(dc) or is_R_decomposition

def is_R_accuracy(acc):
  if type(acc) is robjects.Matrix:
    cnames = colnames(acc)
    r, c = dim(acc)
    if ('matrix' in cls(acc) 
        and 'MASE' in cnames 
        and r in {1,2} and c in {7,8}):
      return True
  return False
  
def is_R_ts(x):
  return type(x) is robjects.FloatVector and 'ts' in cls(x)

def is_R_matrix(x):
  return type(x) is robjects.Matrix and 'matrix' in cls(x)
  





