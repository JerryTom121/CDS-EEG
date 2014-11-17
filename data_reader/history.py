HISTORY_SIZE = 50

class History:
  def __init__(self):
    self.history = []

  def add(self, entry):
    if len(self.history) > HISTORY_SIZE:
      self.history.pop(0)
    self.history.append(entry)

  def had_true(self):
    for e in self.history:
      if e:
        return True
    return False