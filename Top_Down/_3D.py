import pyglet
from Low_Level import LowLevel
from Resources.Overlays import WHITE, _TemplateOverlay
from Resources.Rendering import _ElementTemplate
from Resources.Math import Vector


class Template3d(_ElementTemplate):
    dimension = 3
    _vertex_type = "v3f"

    def _initialize(self):
        super(Template3d, self)._initialize()
        self._switch_coordinate_system()

    def moveTo(self, x: float, y: float, z: float):
        cx, cy, cz = self.location
        dx, dy, dz = x - cx, y - cy, z - cz
        self.move(dx, dy, dz)

    def move(self, dx: float, dy: float, dz: float):
        x, y, z = self.location
        self.location = Vector(x+dx, y+dy, z+dz)
        dx = -dx
        self.vertices = [(x+dx, y+dy, z+dz) for x, y, z in self.vertices]
        self.update()

    def update(self):
        # self._switch_coordinate_system()
        super(Template3d, self).update()
        # self._switch_coordinate_system()

    def rotate(self, pitch=0, yaw=0, roll=0):
        pass

    def _get_vertex_list(self):
        return super(Template3d, self)._get_vertex_list()  # self._create_vertex_list(self.vertices, self.overlay)

    def _switch_coordinate_system(self):
        x, y, z = self.location
        self.location = -x, y, z


class Figure(Template3d):  # basic 3d thing
    mode = pyglet.graphics.GL_POLYGON


class LowerDimensional(Template3d):  # putting stuff in _2d into 3d space
    pass


# todo clean this up - also improve location
class RectPrism(Figure):
    mode = pyglet.graphics.GL_QUADS

    def __init__(self, pos: tuple, l: float, w: float, h: float, texture: _TemplateOverlay = WHITE):
        super(RectPrism, self).__init__(texture)
        pos = LowLevel.convert_pos(pos)
        self.location = pos
        self.length = l
        self.width = w
        self.height = h
        self.vertices = self._get_vertices()
        self._establish_faces()
        self._initialize()

    def _establish_faces(self):
        self.set_top_texture(self.overlay)
        self.set_bottom_texture(self.overlay)
        self.set_front_texture(self.overlay)
        self.set_back_texture(self.overlay)
        self.set_right_texture(self.overlay)
        self.set_left_texture(self.overlay)

    def _create_vertex_list(self, verts: tuple, overlay: _TemplateOverlay):
        return pyglet.graphics.vertex_list(4, (self._vertex_type, verts), overlay.lower_level(self._raw_to_points(verts)))

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
        return super(RectPrism, self)._get_vertex_list()  # self._establish_faces()

    def render(self):  # todo implent batch rendering here
        self.top.draw(self.mode)
        self.bottom.draw(self.mode)
        self.front.draw(self.mode)
        self.back.draw(self.mode)
        self.left.draw(self.mode)
        self.right.draw(self.mode)


class Cube(RectPrism):
    def __init__(self, pos: tuple, side_length: float, texture: _TemplateOverlay = WHITE):
        super(Cube, self).__init__(pos, side_length, side_length, side_length, texture)
