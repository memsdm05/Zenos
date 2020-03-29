import pyglet
from math import *
from Resources.Overlays import WHITE, _TemplateOverlay
from Resources.Rendering import _ElementTemplate
from Resources.Math import Vector, distance
from Low_Level import LowLevel
from _3D import LowerDimensional
from copy import deepcopy

# utility functions
convert_pos = LowLevel.convert_pos


def towards(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1
    angle = atan(dy / dx) if dx != 0 else pi / 2 if dy > 0 else 3 * pi / 2
    angle += pi if dx < 0 else 0
    return angle


def rotate_polygon(list_of_points, rotation, center):
    center_x, center_y = center
    x_cordinates = []
    y_cordinates = []

    for x, y in list_of_points:
        x_cordinates.append(x-center_x)
        y_cordinates.append(y-center_y)
    point_matrix = []
    point_matrix.append(x_cordinates)
    point_matrix.append(y_cordinates)

    rotation = radians(rotation)
    rotation_matrix = [
        [cos(rotation), -sin(rotation)],
        [sin(rotation), cos(rotation)]
    ]

    result = [[], []]
    for i in range(len(x_cordinates)):  # result = R * thing1
        result[0].append(0)
        result[1].append(0)
    for i in range(len(rotation_matrix)):
        # iterate through columns of Y
        for j in range(len(point_matrix[0])):
            # iterate through rows of Y
            for k in range(len(point_matrix)):
                result[i][j] += rotation_matrix[i][k] * point_matrix[k][j]

    polygon = []
    for x, y in zip(result[0], result[1]):
        polygon.append((x + center_x, y + center_y))

    return polygon


def reflect():
    pass


# layout for what everything should have
class _Template_2d(_ElementTemplate):
    dimension = 2
    _pending3D = False
    mode = pyglet.graphics.GL_LINES
    _vertex_type_base = "v2f"

    def __new__(cls, pos, *args, **kwargs):
        is_list = type(pos) == list
        example_pos = pos[0] if is_list else pos
        dimension = len(example_pos)
        if dimension == 3:
            if is_list:
                cls._pending3D = pos
                pos = [(x, y) for x, y, z in pos]
            else:
                pos = pos[0], pos[1]
                cls._pending3D = pos[2]
        args = (pos, *args)
        return super(_Template_2d, cls).__new__(cls)

    def __init__(self, overlay):
        super(_Template_2d, self).__init__(overlay)
        self.rotation = 0

    def _initialize(self):
        if self._pending3D is not False:
            if self._pending3D == list:
                self._convert_to3d(self._pending3D)
                self.hide()
            else:
                self._convert_to3d([(x, y, self._pending3D) for x, y in self.vertices])
        else:
            super(_Template_2d, self)._initialize()

    def moveTo(self, pos=None, rotation=None):
        pos = convert_pos(pos)
        x1, y1 = pos
        x2, y2 = self.location
        dx = 0 if pos is None else x1 - x2
        dy = 0 if pos is None else y1 - y2
        dr = 0 if rotation is None else rotation-self.rotation
        self.move(dx, dy, dr)

    def move(self, dx=0, dy=0, rotation=0):
        change = False
        if dx != 0 or dy != 0:
            change = True
            self.vertices = [(x+dx, y+dy) for x, y in self.vertices]
            x, y = self.location
            self.location = Vector(x + dx, y + dy)
        if self.rotation != 0:
            change = True
            self._rotate(rotation)
        if change:
            self.update()

    def _rotate(self, amount):
        self.rotation += amount
        self.vertices = rotate_polygon(self.vertices, amount, self._find_center())

    def _convert_to3d(self, new_verts):
        self._pending3D = False
        self.vertices = new_verts

    def get_3D_version(self, pos):
        pos = convert_pos(pos)
        x, y, z = pos
        dx, dy = Vector.from_2_points(self.location, (x, y))
        verts = deepcopy(self.vertices)
        self._convert_to3d([(x+dx, y+dy, 0) for x, y in self.vertices])
        new = LowerDimensional(self)
        self.vertices = verts
        return new

    def _convert_pos(self, pos):
        return convert_pos((pos[0], pos[1]))


class Text(_ElementTemplate):
    dimension = 2

    def __init__(self, pos, str, font_size, font_color=WHITE):
        super(Text, self).__init__(font_color)
        self.location = convert_pos(pos)
        self.x, self.y = self.location
        self.msg = str
        self.font_size = font_size
        self.label = self._get_label()

    def _get_label(self):
        return pyglet.text.Label(self.msg, font_name="Times New Roman", font_size=self.font_size,
                                 x=self.x, y=self.y, color=self.overlay.raw())

    def update(self):
        self.label = self._get_label()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.location = self.x, self.y

    def set_string(self, s):
        self.msg = str(s)
        self.update()

    def render(self):
        self.label.draw()


class Shape(_Template_2d):
    mode = pyglet.graphics.GL_POLYGON
    _outline = pyglet.graphics.GL_LINE_LOOP

    def __init__(self, overlay: _TemplateOverlay):
        super(Shape, self).__init__(overlay)
        self.texture = overlay
        # self.outline_color = None
        # self.fill_color = None

    def render_outline(self):
        self.vertex_list.draw(self._outline)


class Polygon(Shape):
    def __init__(self, list_of_points: list, color: _TemplateOverlay = WHITE):
        super(Polygon, self).__init__(color)
        self.vertices = [self._convert_pos(pos) for pos in list_of_points]
        self.length = len(list_of_points)
        self.location = self._find_center()
        self._initialize()


class RegularPolygon(Polygon):
    def __init__(self, center, radius):
        super(RegularPolygon, self).__init__()


class Rectangle(Polygon):
    _mode = pyglet.graphics.GL_QUADS

    def __init__(self, pos: tuple, w: float, h: float, texture: _TemplateOverlay = WHITE):
        pos = self._convert_pos(pos)
        x, y = pos
        vertices = [(x, y), (x + w, y), (x + w, y - h), (x, y - h)]
        super(Rectangle, self).__init__(vertices, texture)
        self.location = pos
        # self.vertices = vertices


class Square(Rectangle):
    def __init__(self, point: tuple, side: float, texture: _TemplateOverlay = WHITE):
        Rectangle.__init__(self, point, side, side, texture)


class Line(_Template_2d):
    _mode = pyglet.graphics.GL_LINE

    def __init__(self, pos1, pos2, overlay=WHITE):
        super(Line, self).__init__(overlay)
        self.texture = overlay
        pos1 = self._convert_pos(pos1)
        pos2 = self._convert_pos(pos2)
        self.vertices = [pos1, pos2]
        x1, y1 = pos1
        x2, y2 = pos2
        self.pos1 = pos1
        self.pos2 = pos2
        self.dx = x2 - x1
        self.dy = y2 - y1
        self.slope = self.dy / self.dx if self.dx != 0 else 0
        self._initialize()


class Point(_Template_2d):
    _mode = pyglet.graphics.GL_POINT

    def __init__(self, x, y, color=WHITE):
        super(Point, self).__init__(color)
        x, y = self._convert_pos((x, y))
        self.texture = color
        self.vertices = [(x, y)]
        self.x = x
        self.y = y
        self.pos = x, y
        self._initialize()


class Ellipse(Shape):
    def __init__(self, pos: tuple, horizontal_radius: float, vertical_radius: float, overlay: _TemplateOverlay = WHITE):
        super(Ellipse, self).__init__(overlay)
        pos = self._convert_pos(pos)
        self.horizontal_radius = horizontal_radius
        self.vertical_radius = vertical_radius
        self.location = pos
        self.horizontal_diameter = 2 * self.horizontal_radius
        self.vertical_diameter = 2 * self.vertical_radius
        self.area = pi * horizontal_radius * vertical_radius
        self.perimeter = self._perimeter()
        self._resolution = self.perimeter // 2  # number of vertices
        self.vertices = self._get_verts()
        self._initialize()

    def _get_verts(self):
        verts = []
        cx, cy = self.location
        for i in range(int(self._resolution)):
            angle = radians(float(i) / self._resolution * 360.0)
            x = self.horizontal_radius * cos(angle) + cx
            y = self.vertical_radius * sin(angle) + cy
            verts.append((x, y))
        return verts

    def _perimeter(self):
        a, b = self.horizontal_radius, self.vertical_radius
        return pi * (3 * (a + b) - sqrt((3 * a + b)*(a + 3 * b)))


class Circle(Ellipse):  # could change to regular polygon
    def __init__(self, pos, radius, texture=WHITE):
        self.radius = radius
        self.diameter = radius * 2
        super(Circle, self).__init__(pos, radius, radius)
        self.texture = self.texture()

    def _perimeter(self):
        return 2 * pi * self.radius

    def distance(self, point):
        return distance(self.location, point) - self.radius
