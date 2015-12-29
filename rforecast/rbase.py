from rpy2 import robjects

def cls(x):
  try:
    return list(robjects.r('class')(x))
  except NotImplementedError:
    raise ValueError('Cannot call R function on Python object.')

def colnames(x):
  try:
    out = robjects.r('colnames')(x)
    if out is robjects.NULL:
      raise ValueError('Object does not have colnames attribute.')
    else:
      return list(out)
  except NotImplementedError:
    raise ValueError('Cannot call R function on Python object.')

def dim(x):
  try:
    out = robjects.r('dim')(x)
    if out is robjects.NULL:
      raise ValueError('Object does not have dim attribute.')
    else:
      return list(out)
  except NotImplementedError:
    raise ValueError('Cannot call R function on Python object.')