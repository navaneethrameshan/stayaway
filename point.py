class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Nearestneighbour:
    def __init__(self, from_point, nearest_neighbour, distance ):
        self.from_point = from_point
        self.nearest_neighbour = nearest_neighbour
        self.distance = distance

    def get_from_point(self):
        return self.from_point

    def get_nearest_neighbour(self):
        return self.nearest_neighbour

    def get_distance(self):
        return self.distance