"""
Connects the user to an arduino

.. moduleauthor:: Vitchyr Pong <vitchyr@gmail.com>
"""
import serial

PORT = 'COM6'
BAUD_RATE = 9600 

def get_arduino():
  """
  Returns an arduino object.
  """
  return serial.Serial(PORT, BAUD_RATE)