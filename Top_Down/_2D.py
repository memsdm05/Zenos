import pyglet
from math import *
from Resources import WHITE, Texture, Color, Gradient, Group
from Low_Level import LowLevel

# utility functions
convert_pos = LowLevel.convert_pos


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx*dx + dy*dy)


def towards(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    angle = atan(dy / dx) if dx != 0 else pi / 2 if dy > 0 else 3 * pi / 2
    angle += pi if dx < 0 else 0
    return angle


def rotate(list_of_points, amount, center=None):
    pass


def reflect():
    pass


# layout for what everything should have
class Template_2d:
    type = 2
    _indexed = False
    _mode = pyglet.graphics.GL_LINES

    def __init__(self):
        self.vertices = None
        self.vertex_list = None
        self.texture = None
        self.center = None
        self.group = None

    def render(self):
        self.vertex_list.draw(self._mode)

    def moveTo(self, pos):
        pos = convert_pos(pos)
        x1, y1 = pos
        x2, y2 = self.center
        dx = x1 - x2
        dy = y1 - y2
        self.move(dx, dy)

    def rotate(self, amount):
        self.vertices = rotate(self.vertices, amount, self.center)
        self.update()

    def move(self, dx, dy, rotation=None):
        if rotation is not None:
            self.vertices = rotate(self.vertices, self.center)

        self.vertices = [(x+dx, y+dy) for x, y in self.vertices]
        self.update()

    def update(self):
        self.vertex_list = self._get_vertex_list()
        self.center = self._find_center()

    def set_texture(self):
        pass

    def _get_vertex_list(self):
        mode = self._vertex_type()
        length = len(self.vertices)
        position_data = self._convert_verticies()
        if self._indexed:
            verticies = pyglet.graphics.vertex_list_indexed(length, [i for i in range(length)], (mode, position_data))
        else:
            verticies = pyglet.graphics.vertex_list(length, (mode, position_data))
        return verticies

    def _convert_verticies(self):
        position_data = []
        for point in self.vertices:
            position_data.extend(point)
        position_data = tuple(position_data)
        return position_data

    def _vertex_type(self):
        data_type = 'i' if type(self.vertices[0][0]) == int else 'f'  # specify integer or float
        return "v2" + data_type

    def pair(self, other):
        if self.group is None:
            if other.group is None:  # neither are in group
                new_group = Group()
                new_group.add(other)
                new_group.add(self)
                return new_group
            else:  # other in group
                other.group.add(self)
        else:  # if this already part of a group
            if other.group is None:
                self.group.add(other)
            else:  # both part of a group
                self.group.add(other.group)

    def unpair(self, other):
        self.group.remove(other)

    def __add__(self, other):
        self.pair(other)

    def __sub__(self, other):
        self.unpair(other)

    def _find_center(self):
        all_x = [x for x, y in self.vertices]
        all_y = [y for x, y in self.vertices]
        return sum(all_x) // len(all_x), sum(all_y) // len(all_y)


class Shape(Template_2d):
    _mode = pyglet.graphics.GL_POLYGON
    _outline = pyglet.graphics.GL_LINE_LOOP

    def __init__(self, texture):
        super(Shape, self).__init__()
        self.texture = texture
        self.outline_color = None
        self.fill_color = None

    def _get_vertex_list(self):
        # data_type = 'i' if type(self.vertices[0][0]) == int else 'f'  # specify integer or float
        vertex_format = "v2i"
        amount_of_sides = len(self.vertices)
        if self.group is None:
            if type(self.texture) is Texture:
                return pyglet.graphics.vertex_list(amount_of_sides, vertex_format, )
            elif type(self.texture) is Color:
                return pyglet.graphics.vertex_list(amount_of_sides, (vertex_format, self._convert_verticies()), self.texture.low_level(self))
            elif type(self.texture) is Gradient:
                pass

    def render_outline(self):
        self.vertex_list.draw(self._outline)


class Polygon(Shape):
    def __init__(self, list_of_points, color=WHITE):
        super(Polygon, self).__init__(color)
        self.vertices = [convert_pos(pos) for pos in list_of_points]
        self.length = len(list_of_points)
        self.lines = []
        for i in range(self.length):
            p1 = list_of_points[i]
            p2 = list_of_points[0] if i == self.length - 1 else list_of_points[i + 1]
            self.lines.append(Line(p1, p2))
        self.update()


class RegularPolygon(Polygon):
    def __init__(self, center, radius):
        super(RegularPolygon, self).__init__()


class Rectangle(Polygon):
    def __init__(self, pos, w, h, texture=WHITE):
        x, y = pos
        self.center = convert_pos(pos)
        vertices = ((x, y), (x + w, y), (x + w, y + h), (x, y + h))
        self.vertices = vertices
        super(Rectangle, self).__init__(vertices, texture)


class Square(Rectangle):
    def __init__(self, point, side, texture=WHITE):
        Rectangle.__init__(self, point, side, side, texture)


class Line(Template_2d):
    _mode = pyglet.graphics.GL_LINE

    def __init__(self, pos1, pos2, color=WHITE):
        super(Line, self).__init__()
        self.texture = color
        pos1 = convert_pos(pos1)
        pos2 = convert_pos(pos2)
        self.vertices = [pos1, pos2]
        x1, y1 = pos1
        x2, y2 = pos2
        self.pos1 = pos1
        self.pos2 = pos2
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.slope = self.dy / self.dx if self.dx != 0 else 0
        self.update()


class Point(Template_2d):
    _mode = pyglet.graphics.GL_POINT

    def __init__(self, x, y, color=WHITE):
        super(Point, self).__init__()
        x, y = convert_pos((x, y))
        self.texture = color
        self.vertices = [(x, y)]
        self.x = x
        self.y = y
        self.pos = x, y
        self.update()


class Ellipse(Shape):
    def __init__(self, pos, horizontal_radius, vertical_radius, color=WHITE):
        super(Ellipse, self).__init__(color)
        pos = convert_pos(pos)
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius
        self.center = pos
        self.horizontal_diameter = 2 * self.horizontal_radius
        self.vertical_diameter = 2 * self.vertical_radius
        self.area = pi * horizontal_radius * vertical_radius
        self.perimeter = self._perimeter()
        self._resolution = self.perimeter // 2  # number of vertices
        self.vertices = self._get_verts()
        self.update()

    def _get_verts(self):
        verts = []
        cx, cy = self.center
        for i in range(int(self._resolution)):
            angle = radians(float(i) / self._resolution * 360.0)
            x = self.horizontal_radius * cos(angle) + cx
            y = self.vertical_radius * sin(angle) + cy
            verts.append((x, y))
        return verts

    def _perimeter(self):
        a, b = self.horizontal_radius, self.vertical_radius
        return pi * (3 * (a + b) - sqrt((3 * a + b)(a + 3 * b)))

    def update(self):
        self.vertices = self._get_verts()
        super(Ellipse, self).update()


class Circle(Ellipse):  # could change to regular polygon
    def __init__(self, pos, radius, texture=WHITE):
        self.radius = radius
        self.diameter = radius * 2
        super(Circle, self).__init__(pos, radius, radius)
        self.texture = texture

    def _perimeter(self):
        return 2 * pi * self.radius

    def distance(self, point):
        return distance(self.center, point) - self.radius
