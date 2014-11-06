MEMORY_SIZE = 40
THRESHOLD = 1.05 # How much larger a rise has to be in order to trigger

class ExtremaChecker:
  def __init__(self):
    self.max_hist = []
    self.min_hist = []

  def add_max(self, m):
    if len(self.max_hist) > MEMORY_SIZE:
      self.max_hist.pop(0)
    self.max_hist.append(m)

  def is_high(self, p):
    if len(self.max_hist) == 0:
      return False
    else:
      total_max = 0
      for m in self.max_hist:
        total_max += m
      return p > (total_max / len(self.max_hist)) * THRESHOLD

  def add_min(self, m):
    if len(self.min_hist) > MEMORY_SIZE:
      self.min_hist.pop(0)
    self.min_hist.append(m)

  def is_low(self, p):
    if len(self.min_hist) == 0:
      return False
    else:
      total_min = 0
      for m in self.min_hist:
        total_min += m
      avg_min = total_min / len(self.min_hist)
      return p < avg_min * (2 - THRESHOLD)