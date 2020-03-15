from math import *  # just steal standard library


class Vector(tuple):
    def __new__(cls, *args):
        cls.args = args
        return tuple.__new__(cls, tuple(args))

    def __add__(self, other):
        return 1

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        return Vector(*[i*other for i in self.args])

    def __pow__(self, power, modulo=None):
        pass

    def magnitude(self):
        return sqrt(sum([i * i for i in self.args]))

    def unit_vector(self):
        x = 1/self.magnitude()
        return self * x

    @staticmethod
    def from_2_points(pos1, pos2):
        vals = [i2 - i1 for i1, i2 in zip(pos1, pos2)]
        return Vector(*vals)
