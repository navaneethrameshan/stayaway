import matplotlib.pyplot as plt
import numpy as np
from analyse import distance
from point import Point
import config
import util
import os
import ast
import numpy
from sklearn import manifold



fig = plt.figure()

count = 0

def animated_plot(old_values, new_value, violation_position, action_status):


    violation_values = np.array([old_values[index] for index in violation_position])
    most_recent_values = np.array([old_values[index] for index in xrange(len(old_values)-config.most_recent_count, len(old_values))])

    old_values = np.delete(old_values, violation_position, 0)

    #figure()
    plt.ion()
    plt.clf()
    plt.plot(old_values[:,0], old_values[:,1], 'x', markersize=10)
    plt.plot(new_value[:,0], new_value[:,1], 'v', color = 'r', markersize=10)
    if len(most_recent_values >0):
        plt.plot(most_recent_values[:,0], most_recent_values[:,1], 'o', color = 'g', markersize=8)


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

    #Save Figure
    global count
    fig.savefig(config.results+str(count) +'.png', bbox_inches=0)
    count+=1

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



def distance_over_time():
    '''
    Load template and plot the distance over time
    '''
    if os.path.isfile("../template"):
        f_handle = open("../template", 'r')
        dynamic_all_values = ast.literal_eval(f_handle.readline())
        violation_position = ast.literal_eval(f_handle.readline())
        f_handle.close()
    else:
        print "No such file"

    X = numpy.array(dynamic_all_values)
    #  print "Actual Values: ",X

    #For all the dimensions normalise the value range between 0 and 1
    #use ceiling function to remove small noise
    X = util.scale(X)

    #n_neighbors = 10
    #Y = manifold.Isomap(n_neighbors, 2, max_iter= 4000).fit_transform(X)
    Y = manifold.MDS().fit_transform(X)

    old_values = Y[:-1]
    new_value = Y[-1:]

    dist =[]
    for index in xrange(0, len(Y)-1):
        dist.append(distance.calculate_distance(Point(Y[index][0], Y[index][1]), Point(Y[index+1][0], Y[index+1][1])))


    plt.plot(dist,'-', color = 'R',markersize = 10, label = "Distance between points")
    plt.xlabel("Time (Mins)")
    plt.ylabel("distance")
    plt.grid(True)
    plt.minorticks_on()
    plt.legend(loc=2)
    plt.show()

    animated_plot(old_values, new_value, violation_position, 'None')



if __name__ == '__main__':
   # old_values = np.array([[0,1],[1,1], [5,5],[6,2], [0,0], [1,2], [2,1], [4,4], [10,10]])
   # new_value = np.array([[3,1]])
   # violation_position = [2,3]
   # animated_plot(old_values, new_value, violation_position, False)
    distance_over_time()
