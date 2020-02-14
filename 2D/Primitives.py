import pyglet
from math import pi

WHITE = (255, 255, 255)


class _Primative():
    def __init__(self, color=WHITE):
        self.color = color

    def render(self):
        pass


class Polygon(_Primative):
    pass


class Quad(Polygon):
    pass


class Rectangle(Quad):
    pass


class Square(Rectangle):
    pass


class Triangle(Polygon):
    pass


class Line(_Primative):
    def __init__(self, point1, point2, color=WHITE):
        super(Line, self).__init__(color)
        x1, y1 = point1.pos
        x2, y2 = point1.pos
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.p1 = point1
        self.p2 = point2
        self.slope = self.dy / self.dx if self.dx != 0 else 0

    def render(self):
        pyglet.graphics.draw()


class Point(_Primative):
    def __init__(self, x, y, color=WHITE):
        super(Point, self).__init__(color)
        self.x = x
        self.y = y
        self.pos = x, y


class Ellipse(_Primative):
    def __init__(self, pos, horizontal_radius, vertical_radius):
        super(Ellipse, self).__init__()
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius
        self.center = pos
        self.horizontal_diameter = 2 * self.horizontal_radius
        self.vertical_diameter = 2 * self.vertical_radius
        self.area = pi * horizontal_radius * vertical_radius


class Circle(Ellipse):
    def __init__(self, pos, radius):
        super(Circle, self).__init__(pos, radius, radius)
        self.radius = radius
        self.diameter = radius * 2

    def distance(self, point):
        pass

