"""
Implments the perceptron algorithm.

.. moduleauthor:: Vitchyr Pong <vitchyr@gmail.com>
"""
from learner.vector import Vector

class Perceptron():
  def __init__(self, raw_training_data=[], labels=[], tolerance=0.05, max_iterations=100, v_array=None):
    """
    Initialize the perceptron learning with the data it learns from.
    The Perceptron instance immediately learns.

    Args:
       raw_training_data (float array array): The data to learn from. Each float array must be the same size.
       labels (int array): The labels of each data point. Each label should be 1 or -1. Must be the same size as training_data.
       tolerance (float): What percent of training data can be wrong.
       max_iterations (int): Maximum number of loops the perceptron algorithm can run without making progress before progrma termiantes
       v_array (int array): A learned vector/array to skip the perceptron algorithm
    """
    if v_array == None:
      training_data = []
      # trick to make data linearly separable by a hyperplane that goes through origin.
      for v in raw_training_data:
        training_data.append(Vector(v+[1]))

      # w is the vector perpendicular to the rule-plane
      self.w = training_data[0].scale(labels[0])

      last_num_points_wrong = len(training_data)
      last_w = self.w
      num_points_wrong = len(training_data)
      no_progress_steps = 0
      iteration = 0
      while num_points_wrong > len(training_data) * tolerance \
        and no_progress_steps < max_iterations:
        iteration += 1
        last_num_points_wrong = num_points_wrong
        num_points_wrong = 0
        for i in range(len(training_data)):
          v = training_data[i].scale(labels[i])
          if self.w*v <= 0: # v is on wrong side of plane
            self.w += v
            num_points_wrong += 1
        print("Perceptron Iteration {0}: percent of wrong points = {1}".format(iteration, num_points_wrong / (len(training_data))))
        if num_points_wrong >= last_num_points_wrong: # didn't improve. Just terminate
          no_progress_steps += 1
    else:
      self.w = Vector(v_array)

  def get_vector(self):
    return self.w

  def label(self, datum):
    input_v = Vector(datum+[1])
    return 1 if input_v*self.w > 0 else -1