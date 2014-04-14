import numpy as np
import sys
from point import Point
from point import Nearestneighbour as NN

def calculate_distance(point1,point2):
    x1 = point1.get_x()
    y1 = point1.get_y()
    x2 = point2.get_x()
    y2 = point2.get_y()

    return (((y2-y1)**2 + (x2-x1)**2)**0.5)

def radius_qos_point(a, b, c, dist):
    return  dist *(a * np.e ** (-(dist-b)**2/(2 * c**2)))

def radius_other_point(a,b,c, dist):
    return  dist-( dist * a * np.e ** (-(dist-b)**2/(2 * c**2)))

def find_nearest_neghbour(point1, numpyarray):

    mindist = sys.float_info.max

    for value in numpyarray:
        dist = calculate_distance(point1, Point(value[0], value[1]))
        if dist < mindist:
            mindist = dist
            nearest_neighbour = NN(point1,Point(value[0], value[1]),mindist)

    return nearest_neighbour

def calculate_distance_list(list1, list2):
    '''
    list1 = [VM1 cpu, VM1 mem, VM2 cpu, VM2 mem, VM3 cpu, ..]
    '''
    dist = None
    if len(list1) == len(list2):
        sum = 0
        for i in xrange(0,len(list1)):
            sum += (float(list2[i])-float(list1[i]))**2
        dist = sum ** 0.5
    else:
        print "MISMATCH in distance calculation"

    return dist

