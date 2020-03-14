import pyglet
import Top_Down.Low_Level
from Top_Down.Resources.Overlays import TemplateOverlay

# todo - clean this shit up
class ElementTemplate:
    mode = None
    dimension = None
    _indexed = True
    _vertex_type = ""

    def __init__(self, overlay: TemplateOverlay):
        self.overlay = overlay
        self.vertices = None
        self.vertex_list = None
        self._raw_points = None
        self.group = Group()
        self.location = None

    def _initialize(self):
        self._raw_points = self.vertices if type(self.vertices[0]) == float else self._points_to_raw(self.vertices)
        self.vertex_list = self.group.add_raw(*self._get_vertex_data(self._raw_points, self.overlay))

    def render(self):
        self.test().draw(self.mode)

    def update(self):
        self._raw_points = self.vertices if type(self.vertices[0]) == float else self._points_to_raw(self.vertices)
        self.vertex_list = self._get_vertex_list()

    def test(self):
        count = len(self.vertices)
        return pyglet.graphics.vertex_list(count, (self._vertex_type, self._raw_points), self.overlay.low_level(count))

    def set_overlay(self, overlay):
        self.overlay = overlay
        self.update()

    def moveTo(self):  # override in other templates
        pass

    def move(self):  # override in other templates
        pass

    def rotate(self):  # override determined by dimensions
        pass

    def _get_vertex_data(self, vertices, overlay):
        count = len(vertices) // self.dimension
        return count, self.mode, [i for i in range(count)], (self._vertex_type, vertices), overlay.low_level(count)

    def _points_to_raw(self, points):
        x = ()
        for pt in points:
            x += pt
        return x

    def _get_vertex_list(self):
        return self._make_vertex_list(self._raw_points, self.overlay)

    def _make_vertex_list(self, vertices, overlay):
        if self.vertex_list is not None:
            self.group.remove(self)
        return self.group.add(self)  # _raw(*self._get_vertex_data(vertices, overlay))

    def pair(self, other):
        other.group.add(self)

    def unpair(self, other):
        self.group.remove(other)

    def __add__(self, other):
        self.pair(other)

    def __sub__(self, other):
        self.unpair(other)


# draw group  # todo make this better
class Group:
    def __init__(self, *args):
        self.type = None
        self.Batch3 = pyglet.graphics.Batch()
        self.Batch2 = pyglet.graphics.Batch()
        self.Batch4 = None
        for item in args:
            self.add(item)

    def render(self):
        low = Low_Level.LowLevel.active
        low.asser2d()
        self.Batch2.draw()
        low.enable3d()
        self.Batch3.draw()

    def add_raw(self, count, mode, indices, position_data, overlay_data):
        dimension = int(position_data[0][1])
        if dimension == 2:
            return self.Batch2.add_indexed(count, mode, None, indices, position_data,
                                           overlay_data)  # count, mode, group, indices, data
        elif dimension == 3:
            return self.Batch3.add_indexed(count, mode, None, indices, position_data, overlay_data)
        else:
            pass

    def add(self, other: ElementTemplate):
        vertex_list = other.vertex_list  # accessing may change
        if other.dimension == 2:
            other_batch = other.group.Batch2
            other_batch.migrate(vertex_list, other.mode, None, self.Batch2)  # vertex list, mode, group, batch
        elif other.dimension == 3:
            other_batch = other.group.Batch3
            other_batch.migrate(vertex_list, other.mode, None, self.Batch3)  # vertex list, mode, group, batch
        else:
            pass
        return vertex_list

    def remove(self, other: ElementTemplate):
        vertex_list = other.vertex_list  # accessing may change
        if other.dimension == 2:
            other_batch = other.group.Batch2
            self.Batch2.migrate(vertex_list, other.mode, None, other_batch)  # vertex list, mode, group, batch
        elif other.dimension == 3:
            other_batch = other.group.Batch3
            self.Batch3.migrate(vertex_list, other.mode, None, other_batch)  # vertex list, mode, group, batch
        else:
            pass

    def __add__(self, other: ElementTemplate):
        return self.add(other)

    def __sub__(self, other: ElementTemplate):
        return self.remove(other)
