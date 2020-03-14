from math import *  # just steal standard library


class Vector(tuple):
    def __new__(cls, *args):
        return tuple.__new__(cls, tuple(args))

    def __add__(self, other):
        return 1

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass