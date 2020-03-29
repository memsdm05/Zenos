import pyglet
from Low_Level import LowLevel
from Resources.Overlays import WHITE, _TemplateOverlay
from Resources.Rendering import _ElementTemplate
from Resources.Math import Vector, distance, Matrix
from math import *


def rotate_3d(list_of_points, center, pitch, yaw, roll):
    dx, dy, dz = center
    translation_vector = Vector([dx, dy, dz])
    point_matrix = Matrix(list_of_points)
    for i, vector in enumerate(point_matrix):
        point_matrix[i] = vector - translation_vector
    x = radians(pitch)
    y = radians(yaw)
    z = radians(roll)
    rotation_matrix = Matrix(
        [cos(z) * cos(y), cos(y) * sin(x) * sin(z) - cos(x) * sin(y), cos(x) * cos(y) * sin(z) + sin(x) * sin(y)],
        [cos(z) * sin(y), cos(x) * cos(y) + sin(x) * sin(z) * sin(y), cos(x) * sin(z) * sin(y)-cos(y) * sin(x)],
        [-sin(z), cos(z) * sin(x), cos(x) * cos(z)]
    )
    rotated_matrix = rotation_matrix * point_matrix
    for i, vector in enumerate(rotated_matrix):
        rotated_matrix[i] = vector + translation_vector
    new_points = [tuple(vector) for vector in rotated_matrix]
    return new_points


class Template3d(_ElementTemplate):
    dimension = 3
    _vertex_type_base = "v3f"

    def __init__(self, overlay):
        super(Template3d, self).__init__(overlay)
        self.rotation = 0, 0, 0

    def _initialize(self):
        super(Template3d, self)._initialize()
        self._switch_coordinate_system()

    def moveTo(self, x: float = None, y: float = None, z: float = None,
               pitch: float = None, yaw: float = None, roll: float = None):
        cx, cy, cz = self.location
        dx = 0 if x is None else x - cx
        dy = 0 if y is None else y - cy
        dz = 0 if z is None else z - cz

        p, ya, r = self.rotation
        dp = 0 if pitch is None else pitch - p
        dya = 0 if yaw is None else yaw - ya
        dr = 0 if roll is None else roll - r
        self.move(dx, dy, dz, dp, dya, dr)

    def move(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0,
             pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0):
        change = False
        if dx != 0 or dy != 0 or dz != 0:
            change = True
            x, y, z = self.location
            self.location = Vector(x+dx, y+dy, z+dz)
            dx = -dx
            self.vertices = [(x+dx, y+dy, z+dz) for x, y, z in self.vertices]
        if pitch != 0 or yaw != 0 or roll != 0:
            change = True
            self._rotate(pitch, yaw, roll)
        if change:
            self.update()

    def _rotate(self, pitch, yaw, roll):
        p, y, r = self.rotation
        self.rotation = p+pitch, y+yaw, r+roll
        self.vertices = rotate_3d(self.vertices, self._find_center(), pitch, yaw, roll)

    def _switch_coordinate_system(self):
        x, y, z = self.location
        self.location = -x, y, z


class Figure(Template3d):  # basic 3d thing
    mode = pyglet.graphics.GL_POLYGON


class LowerDimensional(Figure):  # putting stuff in _2d into 3d space
    function_class = type(distance)
    my_dir = None

    def __init__(self, lower: _ElementTemplate):
        self.my_dir = dir(LowerDimensional) if self.my_dir is None else self.my_dir  # keep all the 3d class variables
        attributes = self.get_attributes(lower)
        super(LowerDimensional, self).__init__(lower.overlay)
        for name, attribute in attributes:
            setattr(self, name, attribute)
        self.location = self._find_center()
        self.rotation = 0, lower.rotation, 0
        self._vertex_type = self._vertex_type_base
        self._initialize()
        lower.hide()
        del lower

    def get_attributes(self, lower):
        a = []
        lower_attr = dir(lower)
        for attribute_name in lower_attr:
            attribute = getattr(lower, attribute_name)
            if type(attribute) != self.function_class and not hasattr(LowerDimensional, attribute_name):
                a.append((attribute_name, attribute))
        return a


# todo clean this up - also improve location
class RectPrism(Figure):
    mode = pyglet.graphics.GL_QUADS

    def __init__(self, pos: tuple, l: float, w: float, h: float, texture: _TemplateOverlay = WHITE, group=None):
        super(RectPrism, self).__init__(texture)
        pos = LowLevel.convert_pos(pos)
        self.location = pos
        self.length = l
        self.width = w
        self.height = h
        self.vertices = self._get_vertices()
        # self._establish_faces()
        self._initialize()

    # def _establish_faces(self):
    #     self.set_top_texture(self.overlay)
    #     self.set_bottom_texture(self.overlay)
    #     self.set_front_texture(self.overlay)
    #     self.set_back_texture(self.overlay)
    #     self.set_right_texture(self.overlay)
    #     self.set_left_texture(self.overlay)

    def _create_vertex_list(self, verts: tuple, overlay: _TemplateOverlay):
        return pyglet.graphics.vertex_list(4, (self._vertex_type, verts), overlay.lower_level(self._raw_to_points(verts)))

    # def _make_rect_prism(self):
    #     if self.vertex_list is not None:
    #         self.vertex_list.delete()
    #     if type(self._top_texture) == Texture:
    #         return self.group.add_raw(24) # count, mode, group, indices, position, overlay
    #     else:  # color and gradients are made seperately
    #         pass

    def _get_vertices(self):
        return self._get_all_vertices()

    def _get_all_vertices(self):
        return self._get_bottom() + self._get_top() + self._get_front() + self._get_back() + self._get_right() + self._get_left()

    def _get_creation_info(self):
        x, y, z = self.location
        dx, dy, dz = self.width / 2, self.height / 2, self.length / 2
        return x, y, z, dx, dy, dz

    def _get_top(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x - dx, y + dy, z - dz, x - dx, y + dy, z + dz, x + dx, y + dy, z + dz, x + dx, y + dy, z - dz

    def _get_bottom(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x - dx, y - dy, z - dz, x + dx, y - dy, z - dz, x + dx, y - dy, z + dz, x - dx, y - dy, z + dz

    def _get_front(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x - dx, y - dy, z + dz, x + dx, y - dy, z + dz, x + dx, y + dy, z + dz, x - dx, y + dy, z + dz

    def _get_back(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x + dx, y - dy, z - dz, x - dx, y - dy, z - dz, x - dx, y + dy, z - dz, x + dx, y + dy, z - dz

    def _get_right(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x - dx, y - dy, z - dz, x - dx, y - dy, z + dz, x - dx, y + dy, z + dz, x - dx, y + dy, z - dz

    def _get_left(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x + dx, y - dy, z + dz, x + dx, y - dy, z - dz, x + dx, y + dy, z - dz, x + dx, y + dy, z + dz
    '''
    def set_top_texture(self, texture: _TemplateOverlay):
        self._top_texture = texture
        self.top = self._create_vertex_list(self._get_top(), self._top_texture)

    def set_bottom_texture(self, texture: _TemplateOverlay):
        self._bottom_texture = texture
        self.bottom = self._create_vertex_list(self._get_bottom(), self._bottom_texture)

    def set_front_texture(self, texture: _TemplateOverlay):
        self._front_texture = texture
        self.front = self._create_vertex_list(self._get_front(), self._front_texture)

    def set_back_texture(self, texture: _TemplateOverlay):
        self._back_texture = texture
        self.back = self._create_vertex_list(self._get_back(), self._back_texture)

    def set_right_texture(self, texture: _TemplateOverlay):
        self._right_texture = texture
        self.right = self._create_vertex_list(self._get_right(), self._right_texture)

    def set_left_texture(self, texture: _TemplateOverlay):
        self._left_texture = texture
        self.left = self._create_vertex_list(self._get_left(), self._left_texture)

    def _get_vertex_list(self):
        # self._establish_faces()
        return super(RectPrism, self)._get_vertex_list()  # self._establish_faces()

    def render(self):  # todo implent batch rendering here
        super(RectPrism, self).render()
        return
        self.top.draw(self.mode)
        self.bottom.draw(self.mode)
        self.front.draw(self.mode)
        self.back.draw(self.mode)
        self.left.draw(self.mode)
        self.right.draw(self.mode)
        
    '''

    def distance(self, pt: tuple):
        x, y, z, dx, dy, dz = self._get_creation_info()
        x2, y2, z2 = pt
        x1 = x-dx if x2 < x-dx else x2 if x2 < x+dx else x+dx
        y1 = y - dy if y2 < y - dy else y2 if y2 < y + dy else y + dy
        z1 = z - dz if z2 < z - dz else z2 if z2 < z + dz else z + dz
        return distance((x1, y1, z1), pt) \
               * -1 if x1 == x+dx and y1 == y+dy and z1 == z+dz else 1  # reverse if inside cube


class Cube(RectPrism):
    def __init__(self, pos: tuple, side_length: float, texture: _TemplateOverlay = WHITE):
        super(Cube, self).__init__(pos, side_length, side_length, side_length, texture)
