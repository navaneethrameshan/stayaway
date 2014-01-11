import matplotlib.pyplot as plt
import numpy as np
from analyse import distance
from point import Point
import config
fig = plt.figure()

def animated_plot(old_values, new_value, violation_position, action_status):
    violation_values = np.array([old_values[index] for index in violation_position])
    old_values = np.delete(old_values, violation_position, 0)

    #figure()
    plt.ion()
    plt.clf()
    plt.plot(old_values[:,0], old_values[:,1], 'x', markersize=10)
    plt.plot(new_value[:,0], new_value[:,1], 'v', color = 'r', markersize=10)

    if len(violation_values) > 0:
        plt.plot(violation_values[:,0], violation_values[:,1], '*', color = 'r', markersize=11)

    # Find nearest points to violations
    for value in violation_values:
        nnviolations = distance.find_nearest_neghbour(Point(value[0], value[1]), old_values)
        violation_center = nnviolations.get_from_point()
        neighbour_center = nnviolations.get_nearest_neighbour()
        dist = nnviolations.get_distance()
        add_circle(plt, violation_center, neighbour_center, dist)

    #scatter(X[:,0], X[:,1])
    fig.suptitle('Action Status: '+ str(action_status))
    plt.grid(True)
    plt.draw()
    plt.pause(1)
    #show()


def add_circle(plt, violation_center, other_center, dist):
    ax = plt.axes()
    qos_circle = plt.Circle((violation_center.get_x(), violation_center.get_y()), 0.75, color='R', fill = True, alpha = 0.3)
    other_circle1 = plt.Circle((other_center.get_x(), other_center.get_y()), 0.75, color='B', fill = True, alpha = 0.2)
    #qos_circle.center = (x1, y1)
    qos_circle.radius = distance.radius_qos_point(config.a, config.b, config.c, dist)
    #plt.plot(x1,y1, 'x', color = 'R')
    ax.add_patch(qos_circle)

    other_circle1.radius = distance.radius_other_point(config.a, config.b, config.c, dist)
    ax.add_patch(other_circle1)


if __name__ == '__main__':
    old_values = np.array([[0,1],[1,1], [5,5],[6,2], [0,0], [1,2], [2,1], [4,4], [10,10]])
    new_value = np.array([[3,1]])
    violation_position = [2,3]
    animated_plot(old_values, new_value, violation_position, False)
