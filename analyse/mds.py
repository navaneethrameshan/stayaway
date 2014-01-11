from plot import plot
from sklearn import manifold, datasets
import numpy
import matplotlib.pyplot as plt
import util

import ast

plt.ion()
dynamic_all_values = []
violation_position = []
closest_range_position = []

def iso_map_static(all_values):
    """
    all_values in list of list format [[VM1cpu,Vm1 mem, vm2cpu, vm2mem],[],..]
    """

    print len(all_values)
   # file =open("VM.classes", 'rb')
   # label = np.array(ast.literal_eval(file.readline()))

    X = numpy.array(all_values)
    print "Actual Values: ",X

    #For all the dimensions normalise the value range between 0 and 1
    #use ceiling function to remove small noise
    X = util.scale(X)

    for i in xrange(12,len(all_values)):

        print len(X[0])

        print X[:i]
        n_neighbors = 10
        #Y = manifold.Isomap(n_neighbors, 2, max_iter= 4000).fit_transform(X)
        Y = manifold.MDS().fit_transform(X[:i])

        #Y = manifold.LocallyLinearEmbedding().fit_transform(X)
        old_values = Y[:-1]
        new_value = Y[-1:]
        plot.animated_plot(old_values, new_value)



def iso_map_dynamic(current_value_list, label, transition, closest_monitor_range, action_status):

    dynamic_all_values.append(current_value_list)


    if(len(dynamic_all_values) > 12):

        X = numpy.array(dynamic_all_values)
      #  print "Actual Values: ",X

        #For all the dimensions normalise the value range between 0 and 1
        #use ceiling function to remove small noise
        X = util.scale(X)

        #n_neighbors = 10
        #Y = manifold.Isomap(n_neighbors, 2, max_iter= 4000).fit_transform(X)
        Y = manifold.MDS().fit_transform(X)

        #Y = manifold.LocallyLinearEmbedding().fit_transform(X)
        old_values = Y[:-1]
        new_value = Y[-1:]
        plot.animated_plot(old_values, new_value, violation_position, action_status)

    if closest_monitor_range:
        closest_range_position.append(len(dynamic_all_values) -1)

    # If transition, remove all the values until the closest_range_position
    # remove matching violation_position. It is important to do this before violation position is included inorder to feed in the updated (correct)
    # position of dynamic_values to violation_position.
    if transition:
        print "!!!!!!!!!!Transition detected!!!!!!!!!! "
        print "Closest Range positions (before): " ,closest_range_position
        print "Violation positions (before) ", violation_position
        print "Length All Values (before): ", len(dynamic_all_values)

        # reversed is important. Remove elements at the end first to avoid messing up index in subsequent deletions.
        for position in reversed(xrange(closest_range_position[-2], closest_range_position[-1])):
            print "Deleting element in position: ", position
            del dynamic_all_values[position]
            if position in violation_position:
                violation_position.remove(position)

        #closest_Range_position[-1] does not anymore hold the right position. update the position.
        closest_range_position[-1] = closest_range_position[-1] - abs(closest_range_position[-2] - closest_range_position[-1])

        print "Length All Values (after): ", len(dynamic_all_values)
        print "Violation positions (after) ", violation_position
        print "Closest Range positions (after): " ,closest_range_position

    # Append the position of the violation only after plotting
    # inorder to plot the current value as current point instead of a violation
    if label:
        violation_position.append(len(dynamic_all_values)-1)
        print "Violation Position: ", violation_position



if __name__ == '__main__':
    #gtrace
    iso_map_static([[2.13, 0.001034, 9.537e-07], [2.057, 0.0009699, 1.907e-06], [1.9869999999999999, 0.0009708, 9.537e-07], [82.06, 0.001003, 2.861e-06], [1.849, 0.001005, 9.537e-07], [1.822, 0.001053, 1.907e-06], [1.794, 0.001093, 0.0], [1.797, 0.0009918, 9.537e-07], [1.736, 0.0009365, 4.768e-06], [1.7760000000000002, 0.0009613, 7.629e-06], [1.6629999999999998, 0.0009937, 0.0], [1.617, 0.001003, 0.0], [1.599, 0.000948, 4.768e-06], [1.566, 0.001135, 7.629e-06], [1.593, 0.0009623, 1.907e-06], [1.514, 0.001326, 9.537e-07], [1.555, 0.0009804, 0.0], [1.514, 0.0009508, 0.0], [1.462, 0.001022, 9.537e-07], [1.4540000000000002, 0.001078, 0.0], [1.433, 0.0009575, 0.0], [1.549, 0.0009584, 9.537e-07], [1.537, 0.00123, 9.537e-07], [1.54, 0.0009737, 9.537e-07], [1.468, 0.0009975, 0.0], [1.4949999999999999, 0.001131, 0.0], [1.4160000000000001, 0.001162, 9.537e-07], [1.414, 0.0009594, 9.537e-07], [1.425, 0.0009623, 8.583e-06], [1.379, 0.0009661, 9.537e-07], [1.392, 0.0009251, 0.0], [1.4040000000000001, 0.0009584, 9.537e-07], [1.506, 0.001026, 9.537e-07], [1.387, 0.0009279, 9.537e-07], [1.335, 0.0009451, 0.0], [1.381, 0.0009136, 9.537e-07], [1.353, 0.001047, 1.907e-06], [1.335, 0.001095, 0.0], [1.434, 0.0009995, 0.0], [1.46, 0.0009956, 9.537e-07], [1.433, 0.0009499, 5.722e-06], [1.477, 0.0009432, 9.537e-07], [1.355, 0.0009918, 9.537e-07], [1.283, 0.0009613, 0.0], [1.367, 0.001011, 9.537e-07], [1.273, 0.0009651, 0.0], [1.35, 0.001032, 9.537e-07], [1.236, 0.000967, 6.676e-06], [1.212, 0.0009556, 9.537e-07], [1.2189999999999999, 0.0009375, 0.0], [1.164, 0.0009575, 0.0], [1.23, 0.0009403, 9.537e-07], [1.21, 0.000968, 5.722e-06], [1.202, 0.0009384, 0.0], [1.195, 0.0009041, 9.537e-07], [1.198, 0.0009003, 0.0], [1.149, 0.0009451, 0.0], [1.091, 0.0008574, 5.722e-06], [1.1520000000000001, 0.000844, 0.0], [1.163, 0.0008888, 1.907e-06], [1.149, 0.0008802, 0.0], [1.205, 0.0009012, 9.537e-07], [1.134, 0.0009222, 9.537e-07], [1.073, 0.0008888, 9.537e-07], [1.166, 0.001059, 9.537e-07], [1.149, 0.0008669, 9.537e-07], [1.192, 0.0008917, 0.0], [1.1079999999999999, 0.0008736, 5.722e-06], [1.137, 0.0009708, 0.0], [1.222, 0.0009203, 9.537e-07], [1.2590000000000001, 0.0008907, 9.537e-07], [1.256, 0.0008698, 0.0], [1.26, 0.001305, 9.537e-07], [1.253, 0.0009193, 9.537e-07], [1.256, 0.0009127, 9.537e-07], [1.25, 0.0008583, 9.537e-07], [1.291, 0.0009527, 9.537e-07], [1.2850000000000001, 0.0008698, 9.537e-07], [1.35, 0.0009279, 9.537e-07], [1.448, 0.0009527, 9.537e-07], [1.469, 0.000927, 9.537e-07], [1.414, 0.0009041, 9.537e-07], [1.572, 0.0009918, 9.537e-07], [1.5610000000000002, 0.0009146, 0.0], [1.584, 0.0009251, 3.815e-06], [1.7000000000000002, 0.001139, 1.907e-06], [1.6969999999999998, 0.0009508, 9.537e-07], [1.77, 0.0009899, 9.537e-07], [1.752, 0.0009785, 9.537e-07], [1.9009999999999998, 0.0009727, 9.537e-07], [1.9349999999999998, 0.001076, 1.907e-06], [1.95, 0.0009604, 9.537e-07], [2.0420000000000003, 0.0009565, 5.722e-06], [2.1149999999999998, 0.0009937, 0.0], [2.2089999999999996, 0.001001, 9.537e-07], [2.103, 0.0009575, 9.537e-07], [2.081, 0.0009823, 2.861e-06], [2.176, 0.001232, 9.537e-07], [2.2089999999999996, 0.0009575, 0.0], [2.31, 0.001078, 0.0], [2.243, 0.001152, 0.0], [2.328, 0.001015, 7.629e-06], [2.402, 0.0009918, 1.907e-06], [2.512, 0.0009823, 9.537e-07], [2.383, 0.001373, 6.676e-06], [2.4539999999999997, 0.001253, 9.537e-07], [2.481, 0.001301, 9.537e-07], [2.448, 0.001045, 9.537e-07], [2.533, 0.001013, 9.537e-07], [2.423, 0.001131, 9.537e-07], [2.5669999999999997, 0.00107, 2.861e-06], [2.536, 0.00111, 5.722e-06], [2.545, 0.00169, 2.861e-06], [2.463, 0.001284, 9.537e-07], [2.716, 0.001068, 9.537e-07], [2.5669999999999997, 0.001251, 9.537e-07], [2.548, 0.001141, 9.537e-07], [2.7369999999999997, 0.00104, 9.537e-07], [2.673, 0.001091, 9.537e-07], [2.768, 0.001125, 9.537e-07], [2.774, 0.001015, 4.768e-06], [2.6519999999999997, 0.001017, 9.537e-07], [2.716, 0.001015, 1.907e-06], [2.689, 0.001083, 9.537e-07], [2.881, 0.001265, 9.537e-07], [2.859, 0.00131, 2.861e-06], [2.734, 0.001129, 0.0], [2.8930000000000002, 0.00193, 9.537e-07], [2.911, 0.001503, 9.537e-07], [3.0269999999999997, 0.001331, 9.537e-07], [2.9690000000000003, 0.001194, 9.537e-07], [2.899, 0.001081, 9.537e-07], [2.673, 0.001017, 9.537e-07], [2.8289999999999997, 0.001055, 1.907e-06], [2.841, 0.001093, 5.722e-06], [2.884, 0.001045, 9.537e-07], [2.939, 0.001062, 5.722e-06], [3.1559999999999997, 0.001038, 9.537e-07], [3.137, 0.001057, 1.907e-06], [2.9850000000000003, 0.001041, 9.537e-07], [2.963, 0.001032, 0.0], [3.073, 0.001154, 1.907e-06], [3.241, 0.001574, 5.722e-06], [3.229, 0.001091, 1.907e-06], [3.052, 0.001251, 9.537e-07], [3.0269999999999997, 0.001043, 9.537e-07], [3.088, 0.001055, 9.537e-07], [3.1620000000000004, 0.001045, 2.861e-06], [3.2099999999999995, 0.001024, 9.537e-07], [3.2710000000000004, 0.00106, 9.537e-06], [3.2169999999999996, 0.001078, 1.907e-06], [3.198, 0.001101, 9.537e-07], [3.2039999999999997, 0.001293, 0.0], [3.3390000000000004, 0.001301, 1.907e-06], [3.4549999999999996, 0.001467, 1.526e-05], [3.467, 0.001104, 9.537e-07], [3.314, 0.001036, 2.861e-06], [3.32, 0.00106, 9.537e-07], [3.363, 0.001045, 5.722e-06], [3.2779999999999996, 0.001245, 9.537e-07], [3.2960000000000003, 0.001347, 3.815e-06], [3.4299999999999997, 0.00103, 1.907e-06], [3.4479999999999995, 0.001095, 6.676e-06], [3.467, 0.001055, 7.629e-06], [3.5159999999999996, 0.001093, 9.537e-07], [3.5639999999999996, 0.001097, 9.537e-07], [3.583, 0.001066, 9.537e-07], [3.6069999999999998, 0.001209, 9.537e-07], [3.589, 0.001118, 9.537e-07], [3.5220000000000002, 0.001072, 9.537e-07], [3.583, 0.001169, 8.583e-06], [3.5159999999999996, 0.00108, 1.907e-06], [3.6069999999999998, 0.001123, 9.537e-07], [3.497, 0.001087, 1.907e-06], [3.418, 0.001076, 9.537e-07], [3.5340000000000003, 0.001017, 4.768e-06], [3.406, 0.001087, 7.629e-06], [3.5029999999999997, 0.001068, 9.537e-07], [3.6740000000000004, 0.001499, 1.907e-06], [3.6130000000000004, 0.001114, 2.861e-06], [3.6380000000000003, 0.002686, 0.0001974], [3.662, 0.001076, 2.861e-06], [3.6990000000000003, 0.00107, 1.431e-05], [3.7289999999999996, 0.001064, 1.717e-05], [3.833, 0.001078, 4.768e-06], [3.784, 0.001081, 9.537e-07], [3.7289999999999996, 0.001106, 9.537e-07], [3.656, 0.001129, 6.676e-06], [3.662, 0.001186, 5.722e-06], [3.7350000000000003, 0.00115, 1.907e-06], [3.8089999999999997, 0.001146, 9.537e-06], [3.7289999999999996, 0.001091, 9.537e-07], [3.7900000000000005, 0.001099, 1.907e-06], [3.6740000000000004, 0.001101, 2.861e-06], [3.7960000000000003, 0.001125, 9.537e-07], [3.857, 0.001123, 9.537e-07], [3.9, 0.001163, 1.907e-06], [4.0280000000000005, 0.001108, 8.583e-06], [4.071000000000001, 0.001183, 1.907e-06], [3.9, 0.001501, 7.629e-06], [4.016, 0.001114, 2.861e-06], [4.108, 0.001144, 1.144e-05], [4.102, 0.00111, 0.0], [3.943, 0.001114, 9.537e-07], [4.083, 0.001099, 2.861e-06], [4.0649999999999995, 0.001467, 9.537e-07], [4.034, 0.001083, 0.0], [4.132000000000001, 0.001236, 8.583e-06], [3.9370000000000003, 0.001238, 1.907e-06], [3.9370000000000003, 0.001451, 1.907e-06], [4.1259999999999994, 0.001184, 9.537e-07], [4.089, 0.001507, 9.537e-07], [4.095, 0.00112, 9.537e-07], [4.077, 0.001339, 9.537e-07], [4.1259999999999994, 0.001095, 1.907e-06], [4.266, 0.00128, 1.144e-05], [4.047, 0.001114, 1.907e-06], [4.15, 0.001165, 9.537e-07], [4.236, 0.001194, 9.537e-07], [4.468, 0.001392, 1.907e-06], [4.431, 0.001133, 4.768e-06], [4.504, 0.001146, 2.861e-06], [4.547, 0.001146, 1.907e-06], [4.449, 0.002041, 1.907e-06], [4.529, 0.001591, 9.537e-07], [4.553, 0.00132, 1.144e-05], [4.614, 0.001451, 9.537e-07], [4.73, 0.00119, 3.815e-06], [4.559, 0.001125, 3.815e-06], [4.626, 0.001186, 9.537e-07], [4.492, 0.001801, 9.537e-07], [4.590000000000001, 0.001081, 9.537e-07], [4.858, 0.001135, 2.861e-06], [4.913, 0.001589, 2.861e-06], [4.889, 0.001211, 1.907e-06], [4.883, 0.001154, 1.907e-06], [4.791, 0.001152, 4.768e-06], [4.901, 0.001657, 9.537e-07], [4.907, 0.001369, 9.537e-07], [4.993, 0.001144, 8.583e-06], [4.846, 0.001167, 1.907e-06], [4.81, 0.001276, 3.815e-06], [4.822, 0.001348, 9.537e-07], [4.913, 0.001398, 1.907e-06], [4.956, 0.001102, 9.537e-07], [4.846, 0.001177, 1.907e-06], [4.8340000000000005, 0.001173, 1.907e-06], [5.005, 0.001757, 1.907e-06], [4.846, 0.001184, 6.676e-06], [4.8950000000000005, 0.001186, 9.537e-07], [4.944, 0.001173, 9.537e-07], [4.993, 0.001221, 2.861e-06], [4.797, 0.00144, 5.722e-06], [4.974, 0.001768, 9.537e-07], [4.913, 0.001173, 9.537e-07], [4.938, 0.001205, 2.861e-06], [4.913, 0.001205, 1.907e-06], [4.852, 0.001577, 4.768e-06], [0.0, 0.0008001, 0.0003214], [4.761, 0.0009899, 1.907e-06], [4.993, 0.001177, 5.722e-06], [4.938, 0.001497, 1.907e-06], [4.749, 0.001696, 9.537e-07], [4.352, 0.001432, 1.907e-06], [3.955, 0.001434, 7.629e-06], [3.9059999999999997, 0.001455, 9.537e-07], [3.8760000000000003, 0.001797, 8.583e-06], [3.7960000000000003, 0.001436, 1.907e-06], [3.8699999999999997, 0.001442, 2.861e-06], [3.784, 0.001442, 2.861e-06], [3.5770000000000004, 0.001797, 9.537e-07], [3.6740000000000004, 0.001522, 9.537e-07], [3.5029999999999997, 0.001709, 2.861e-06], [3.29, 0.00201, 7.629e-06], [3.18, 0.002186, 5.722e-06], [3.137, 0.001459, 2.861e-06], [2.972, 0.001446, 5.722e-06], [2.927, 0.001738, 1.907e-06], [2.841, 0.001461, 2.861e-06], [2.795, 0.001467, 1.907e-06], [2.762, 0.001436, 3.815e-06], [2.606, 0.001457, 9.537e-07], [2.493, 0.001457, 1.907e-06], [2.402, 0.001415, 1.907e-06], [2.42, 0.001438, 9.537e-07], [2.267, 0.001415, 9.537e-07], [2.161, 0.001411, 9.537e-07], [2.072, 0.001534, 9.537e-07], [2.1479999999999997, 0.002254, 6.676e-06], [1.9380000000000002, 0.001457, 3.815e-06], [1.95, 0.001894, 9.537e-07], [1.892, 0.001598, 2.861e-06], [1.968, 0.001694, 9.537e-07], [1.9380000000000002, 0.001472, 9.537e-07], [1.999, 0.001745, 2.861e-06], [1.865, 0.002209, 9.537e-07], [1.892, 0.00153, 1.907e-06], [1.7819999999999998, 0.00148, 2.861e-06], [1.794, 0.001574, 0.0], [1.7579999999999998, 0.001665, 8.583e-06], [1.743, 0.002518, 9.537e-07], [1.6480000000000001, 0.001848, 9.537e-06], [1.743, 0.001856, 1.907e-06], [1.669, 0.001921, 9.537e-07], [1.6019999999999999, 0.001575, 9.537e-07], [1.624, 0.002121, 0.0], [1.999, 0.002953, 6.199e-05], [1.685, 0.001625, 8.583e-06], [1.59, 0.001455, 1.907e-06], [1.6660000000000001, 0.00172, 3.815e-06], [1.614, 0.001366, 4.768e-06], [1.669, 0.001341, 3.815e-06], [1.617, 0.001665, 2.861e-06], [1.608, 0.001736, 4.768e-06], [1.59, 0.001598, 9.537e-07], [1.7399999999999998, 0.001501, 0.0], [1.633, 0.001513, 9.537e-07], [1.624, 0.00148, 1.907e-06], [1.553, 0.001591, 0.0], [1.5779999999999998, 0.001574, 0.0], [1.584, 0.001621, 9.537e-07], [1.6049999999999998, 0.001616, 9.537e-07], [1.569, 0.00148, 1.907e-06], [1.5559999999999998, 0.001532, 5.722e-06], [1.6199999999999999, 0.001675, 0.0], [1.572, 0.002018, 9.537e-07], [1.358, 0.001719, 9.537e-07], [1.414, 0.001526, 1.907e-06], [1.485, 0.001354, 9.537e-07], [1.418, 0.001602, 0.0], [1.407, 0.001371, 9.537e-07], [1.466, 0.001616, 0.0], [1.52, 0.001383, 0.0], [1.349, 0.001371, 9.537e-07], [1.323, 0.001558, 9.537e-07], [1.3820000000000001, 0.001328, 0.0], [1.381, 0.001413, 0.0], [1.361, 0.001516, 3.815e-06], [1.2919999999999998, 0.001507, 9.537e-07], [1.299, 0.001564, 1.907e-06], [1.273, 0.001839, 9.537e-07], [1.3050000000000002, 0.001589, 1.907e-06], [1.268, 0.00178, 9.537e-07], [1.355, 0.001709, 9.537e-07], [1.366, 0.001486, 9.537e-07], [1.306, 0.001734, 1.907e-06], [1.347, 0.001499, 9.537e-07], [1.257, 0.001835, 1.907e-06], [1.262, 0.001921, 1.907e-06], [1.257, 0.002018, 2.861e-06], [1.25, 0.002148, 9.537e-07], [1.234, 0.00173, 0.0], [1.302, 0.001451, 4.768e-06], [1.262, 0.001429, 1.907e-06], [1.256, 0.001663, 2.861e-06], [1.328, 0.001369, 1.907e-06], [1.282, 0.00135, 9.537e-07], [1.2409999999999999, 0.001545, 9.537e-07], [1.2510000000000001, 0.00169, 3.815e-06], [1.276, 0.00136, 9.537e-07], [1.299, 0.001942, 9.537e-07], [1.317, 0.001751, 9.537e-07], [1.273, 0.001522, 0.0], [1.369, 0.001503, 9.537e-07], [1.381, 0.001543, 9.537e-07], [1.448, 0.00165, 3.815e-06], [1.549, 0.00181, 9.537e-07], [1.52, 0.001381, 3.815e-06], [1.559, 0.001568, 9.537e-07], [1.562, 0.001411, 0.0], [1.584, 0.001389, 9.537e-07], [1.6049999999999998, 0.001814, 9.537e-07], [1.566, 0.001352, 9.537e-07], [1.6969999999999998, 0.001547, 0.0], [1.7760000000000002, 0.002357, 0.0], [1.7819999999999998, 0.002026, 9.537e-07], [1.8800000000000001, 0.001614, 9.537e-07], [1.8950000000000002, 0.001757, 0.0], [1.8519999999999999, 0.001934, 9.537e-07], [1.9929999999999999, 0.001534, 9.537e-07], [1.9869999999999999, 0.001453, 9.537e-07], [2.094, 0.001631, 1.907e-06], [2.158, 0.001812, 2.861e-06], [2.194, 0.001722, 4.768e-06], [2.106, 0.001549, 9.537e-07], [2.084, 0.001745, 0.0], [2.267, 0.002087, 4.768e-06], [2.274, 0.003582, 5.722e-06], [2.3040000000000003, 0.001802, 1.907e-06], [2.31, 0.001656, 9.537e-07], [2.4899999999999998, 0.001991, 9.537e-07], [2.31, 0.001886, 7.629e-06], [2.42, 0.002159, 0.0], [2.4170000000000003, 0.001795, 0.0], [2.472, 0.001593, 9.537e-07], [2.46, 0.001688, 4.768e-06], [2.429, 0.001831, 9.537e-07], [2.484, 0.001862, 1.907e-06], [2.53, 0.001434, 9.537e-07], [2.56, 0.003349, 0.0002117], [2.551, 0.001968, 1.431e-05], [2.5940000000000003, 0.001575, 7.629e-06], [2.6310000000000002, 0.001869, 2.861e-06], [2.7470000000000003, 0.001862, 9.537e-07], [2.686, 0.00157, 1.907e-05], [2.6, 0.001482, 2.003e-05], [2.6759999999999997, 0.001442, 1.907e-06], [2.686, 0.002338, 9.537e-07], [2.698, 0.001543, 9.537e-07], [2.557, 0.00206, 1.621e-05], [2.597, 0.00152, 9.537e-07], [2.6950000000000003, 0.002121, 0.0], [2.731, 0.001976, 1.907e-06], [2.8049999999999997, 0.002689, 1.144e-05], [2.704, 0.001759, 1.907e-06], [2.768, 0.002419, 0.0], [2.856, 0.001961, 9.537e-07], [2.7470000000000003, 0.001471, 1.907e-06], [2.768, 0.001629, 3.815e-06], [2.692, 0.001879, 4.768e-06], [2.6950000000000003, 0.001841, 9.537e-07], [2.78, 0.002144, 2.861e-06], [2.859, 0.002575, 9.537e-07], [2.771, 0.001701, 4.768e-06], [2.795, 0.001469, 9.537e-07], [2.881, 0.001467, 3.815e-06], [2.866, 0.002537, 9.537e-07], [2.9819999999999998, 0.002178, 3.815e-06], [3.061, 0.001585, 5.722e-06], [2.963, 0.001638, 9.537e-07], [2.936, 0.002396, 9.537e-07], [2.911, 0.003605, 9.537e-07], [3.0669999999999997, 0.001844, 1.907e-06], [2.994, 0.001944, 2.861e-06], [3.018, 0.001686, 1.907e-06], [3.0460000000000003, 0.001839, 1.907e-06], [3.1220000000000003, 0.001881, 9.537e-07], [3.2169999999999996, 0.001545, 9.537e-07], [3.082, 0.001518, 0.0], [3.098, 0.00206, 9.537e-07], [3.357, 0.001751, 3.815e-06], [3.302, 0.001648, 1.907e-06], [3.467, 0.001945, 2.861e-06], [3.418, 0.001818, 1.907e-06], [3.424, 0.001524, 9.537e-07], [3.2960000000000003, 0.002232, 9.537e-07], [3.3939999999999997, 0.001707, 9.537e-07], [3.363, 0.002853, 2.861e-06], [3.302, 0.001999, 9.537e-07], [3.363, 0.002193, 8.583e-06], [3.381, 0.002213, 5.722e-06], [3.436, 0.001852, 3.815e-06], [3.3390000000000004, 0.00161, 2.861e-06], [3.406, 0.00161, 9.537e-07], [3.5029999999999997, 0.001726, 6.676e-06], [3.479, 0.002556, 3.815e-06], [3.5340000000000003, 0.002293, 9.537e-07], [3.3689999999999998, 0.001673, 1.907e-06], [3.6069999999999998, 0.001581, 1.907e-06], [3.6069999999999998, 0.001556, 2.861e-06], [3.5220000000000002, 0.001755, 2.861e-06], [3.6380000000000003, 0.002228, 6.676e-06], [3.6189999999999998, 0.002525, 3.815e-06], [3.6130000000000004, 0.002659, 9.537e-07], [3.589, 0.00182, 1.907e-06], [3.6249999999999996, 0.001602, 9.537e-07], [3.6069999999999998, 0.001984, 9.537e-07], [3.6990000000000003, 0.001947, 3.815e-06], [3.6679999999999997, 0.001703, 3.815e-06], [3.833, 0.002136, 4.768e-06], [3.723, 0.001659, 9.537e-07], [3.857, 0.001753, 9.537e-07], [3.882, 0.001694, 2.861e-06], [3.918, 0.001495, 2.861e-06], [3.857, 0.001881, 1.907e-06], [3.7900000000000005, 0.002224, 4.768e-06], [4.089, 0.002251, 5.722e-06], [3.9919999999999995, 0.001766, 2.861e-06], [3.925, 0.002171, 9.537e-07], [4.047, 0.001957, 1.907e-06], [3.9730000000000003, 0.00169, 1.907e-06], [4.047, 0.002251, 1.907e-06], [3.925, 0.001627, 9.537e-07], [4.041, 0.001896, 0.0], [4.022, 0.001564, 9.537e-07], [4.1259999999999994, 0.002075, 2.861e-06], [4.12, 0.00177, 4.768e-06], [4.15, 0.00201, 5.722e-06], [4.053, 0.001688, 9.537e-07], [4.181, 0.001852, 0.0], [4.102, 0.002087, 2.861e-06], [4.0649999999999995, 0.002705, 0.0001841], [3.943, 0.001619, 1.621e-05], [3.949, 0.001547, 5.722e-06], [3.9919999999999995, 0.00206, 1.049e-05], [4.022, 0.002453, 3.815e-06], [4.199, 0.001581, 6.676e-06], [4.175, 0.002693, 1.907e-06], [4.132000000000001, 0.002293, 2.861e-06], [4.022, 0.001665, 5.722e-06]])

    #lxc-cpubomb
    #iso_map_static([[0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0035526, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.002745, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0793659, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0022463, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0034285999999999995, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19664896, 0.0023164, 8577024], [0.0, 19664896, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0020691, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0020652, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0022524, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0022861, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0803744, 19705856, 0.0, 8577024], [0.0, 19705856, 0.0, 8577024], [0.0104306, 19705856, 0.0019969000000000002, 8577024], [0.0, 19746816, 0.0, 8577024], [0.1871809, 19673088, 0.0, 8577024], [84.76662400000001, 19857408, 0.0, 8577024], [99.3736962, 20037632, 0.0, 8577024], [99.6861078, 20037632, 0.0, 8577024], [99.1106006, 20037632, 0.0015858, 8577024], [99.8319596, 20037632, 0.0, 8577024], [99.1290831, 20037632, 0.0, 8577024], [99.5287696, 20037632, 0.0, 8577024]])