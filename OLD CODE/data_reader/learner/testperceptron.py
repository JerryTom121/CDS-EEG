from perceptron import Perceptron
import unittest

class TestPerceptron(unittest.TestCase):
    def setUp(self):
        self.tolerance = 0.0
        self.max_iterations = 1000
        return

    def test_learning_1D(self):
        # A simple 1D test case, where the label is 1 iff the number is postive
        v1 = [-0.5]
        v2 = [0.1]
        v3 = [-2]
        v4 = [-0.9]
        v5 = [1.34]
        v6 = [-1]
        data = [v1, v2, v3, v4, v5, v6]
        labels = [-1, 1, -1, -1, 1, -1]
        p = Perceptron(data, labels, self.tolerance, self.max_iterations)

        self.assertEqual(p.label([5]), 1)
        self.assertEqual(p.label([1]), 1)
        self.assertEqual(p.label([0.2]), 1)
        self.assertEqual(p.label([-1]), -1)
        self.assertEqual(p.label([-1.1]), -1)
        self.assertEqual(p.label([-5]), -1)

    def test_learning_2D(self):
        # A 2D test case, where the label is 1 iff the number is above the y=x line
        v1 = [-0.5, 0]
        v2 = [0, 0.1]
        v3 = [-0.2, 0.1]
        v4 = [-0.9, -0.4]
        v5 = [1.1, 1.4]
        v6 = [-1, 1]
        v7 = [0.5, 0]
        v8 = [0, -0.1]
        v9 = [-2, -3]
        v10 = [-0.4, -0.9]
        v11 = [1.6, 1.2]
        v12 = [1, -1]
        data = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12]
        labels = [1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1,]
        p = Perceptron(data, labels, self.tolerance, self.max_iterations)

        self.assertEqual(p.label([-1, 1]), 1)
        self.assertEqual(p.label([1, 2]), 1)
        self.assertEqual(p.label([-1, 0]), 1)
        self.assertEqual(p.label([1, -1]), -1)
        self.assertEqual(p.label([1, 0]), -1)
        self.assertEqual(p.label([0.4, -.9]), -1)

    def test_2D_threshold(self):
        # A 2D test to see if the perceptron algorithm can handle the threshold being
        # the line y = x + 1
        v1 = [-0.5, 0]
        v2 = [0, 0.1]
        v3 = [-0.2, 0.1]
        v4 = [-0.9, -0.4]
        v5 = [1.1, 1.4]
        v6 = [0.5, 0]
        v7 = [0, -0.1]
        v8 = [-1, 1]
        v9 = [-2, 3]
        v10 = [-0.4, 0.9]
        v11 = [0, 1.2]
        data =   [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11]
        labels = [-1, -1, -1, -1, -1, -1, -1,  1,  1,   1,   1]
        p = Perceptron(data, labels, self.tolerance, self.max_iterations)

        self.assertEqual(p.label([-1.5, 1]), 1)
        self.assertEqual(p.label([1, 5]), 1)
        self.assertEqual(p.label([-2, 0]), 1)
        self.assertEqual(p.label([1, -1]), -1)
        self.assertEqual(p.label([1, 0]), -1)
        self.assertEqual(p.label([0.4, 0.9]), -1)

if __name__ == '__main__':
    unittest.main()