from rpy2 import robjects

def cls(x):
  try:
    return list(robjects.r('class')(x))
  except NotImplementedError:
    raise TypeError('Cannot call R function on Python object.')

def colnames(x):
  try:
    out = robjects.r('colnames')(x)
    if out is robjects.NULL:
      return None
    else:
      return list(out)
  except NotImplementedError:
    raise TypeError('Cannot call R function on Python object.')

def dim(x):
  try:
    out = robjects.r('dim')(x)
    if out is robjects.NULL:
      return None
    else:
      return list(out)
  except NotImplementedError:
    raise TypeError('Cannot call R function on Python object.')