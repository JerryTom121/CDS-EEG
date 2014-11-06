"""
Implement simple n-dimensional vector functions.

I implement my own vector functions because this code will have to be translated to C eventually.

.. moduleauthor: Vitchyr Pong <Vitchyr@gmail.com>
"""
from math import sqrt

class Vector():
  def __init__(self, data):
    """
    Create a vector from an array of floats.

    Args:
      data (float array): the data of the vector
    """
    self.v = data

  def __add__(self, other):
    """
    Add this vector with another vector. Returns a new vector.

    Args:
      other (float array): The other vector

    precon: length of other vector is the same as this vector
    """
    return Vector([a + b for a, b in zip(self.v, other.v)])


  def __mul__(self, other):
    """
    Dot product of this vector with another vector.
    
    Args:
      other (float array): The other vector

    precon: length of other vector is the same as this vector
    """
    accum = 0
    for i in range(len(self.v)):
      accum += self.v[i]*other.v[i]
    return accum
  __rmul__ = __mul__

  def scale(self, scalar):
    """
    Returns a new vector which is the first vector scaled.

    Args
      scalar (float): the scalar.
    """
    return Vector([x*scalar for x in self.v])

  def normalize(self):
    """
    Normalize a vector to have a magnitude of 1. This returns a new vector.
    """
    accum = 0
    for i in range(len(self.v)):
      accum += self.v[i]**2
    accum = sqrt(accum)
    return self.scale(1/accum)

  def to_array(self):
    return self.v

  def __str__(self):
    return str(self.v)