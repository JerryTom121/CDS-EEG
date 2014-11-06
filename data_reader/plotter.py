import matplotlib.pyplot as plt

plt.plotfile('trial.dat', delimiter=' ', cols=(0, 1),
             names=('col1', 'col2'), marker='o')
plt.show()