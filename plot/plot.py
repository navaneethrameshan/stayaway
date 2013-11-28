import matplotlib.pyplot as plt
import numpy as np


def animated_plot(old_values, new_value, violation_position):
    violation_values = np.array([old_values[index] for index in violation_position])
    old_values = np.delete(old_values, violation_position, 0)

    #figure()
    plt.clf()
    plt.plot(old_values[:,0], old_values[:,1], 'x', markersize=10)
    plt.plot(new_value[:,0], new_value[:,1], 'v', color = 'r', markersize=10)

    if len(violation_values) > 0:
        plt.plot(violation_values[:,0], violation_values[:,1], '*', color = 'r', markersize=11)

    #scatter(X[:,0], X[:,1])
    plt.draw()
    plt.pause(5)
    #show()