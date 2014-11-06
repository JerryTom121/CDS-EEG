from state import State
from extremachecker import ExtremaChecker
import time

# Settings Constants
MAX_HIGH_LOW_TIME_GAP = 1 # seconds  

# Contains logic for deciding what to do with the next datum
class DataProcessor():
  def __init__(self):
    self.last_val = 0
    self.state = State.null
    self.is_increasing = False
    self.last_state_switch = time.time()
    self.extrema_checker = ExtremaChecker()

  # Outputs (False, True) if a glance to the right is made
  # Outputs (True, False) if a glance to the left is made
  # Outputs (False, False) otherwise
  def process_datum(self, val):
    # Check if we've reach a max/min
    new_max = self.is_increasing and val < self.last_val
    new_min = not self.is_increasing and val > self.last_val
    
    if new_max or new_min:
      self.is_increasing = not self.is_increasing

    # Handle new maxes and mins
    high = self.is_high(new_max)
    low = self.is_low(new_min)

    # if high:
    #   print("High")
    # if low:
    #   print("Low")
      
    # Check for left glance and right glance
    #   left glance: quick low to high
    #   right glance: quick high to low
    right = False
    left = False
    if high or low:
      # Check if we have a *quick* low-to-high or high-to-low switch
      if time.time() - self.last_state_switch < MAX_HIGH_LOW_TIME_GAP:
        left = high and self.state == State.low
        right = low and self.state == State.high
        if left or right:
          self.state = State.null
      
      self.state = State.high if high else State.low
      self.last_state_switch = time.time()

    self.last_val = val

    return left, right

  # Checks if the new value should trigger a high signal
  def is_high(self, new_max):
    high = False
    if new_max:
      if self.extrema_checker.is_high(self.last_val): # last_val = the new max
        high = True
      self.extrema_checker.add_max(self.last_val)
    return high

  def is_low(self, new_min):
    low = False
    if new_min:
      if self.extrema_checker.is_low(self.last_val): # last_val = the new min
        low = True
      self.extrema_checker.add_min(self.last_val)
    return low

  # Returns true if the max has changed.
  #   If so, the second 
  def check_max(self, val):
    return 