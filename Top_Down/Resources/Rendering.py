import pyglet
from Resources.Overlays import _TemplateOverlay

low = None

# todo - clean this shit up
class _ElementTemplate:
    mode = None
    dimension = None
    _indexed = True
    _vertex_type = ""

    def __init__(self, overlay: _TemplateOverlay):
        self.overlay = overlay
        self.vertices = None
        self.vertex_list = None
        self._raw_points = None
        self.group = Group()
        self.location = None
        self.amount_of_vertices = None
        self.showing = False

    def _initialize(self):
        if type(self.vertices[0]) == float:
            self._raw_points = tuple(self.vertices)
            self.vertices = self._raw_to_points(self._raw_points)
        else:
            self._raw_points = self._points_to_raw(self.vertices)
        self.vertex_list = self.group.add_raw(*self._get_vertex_data(self._raw_points, self.overlay))
        self.amount_of_vertices = len(self._raw_points) // self.dimension

    def render(self):
        self.vertex_list.render()

    def update(self):
        self._raw_points = self._points_to_raw(self.vertices)
        self.vertex_list = self._get_vertex_list()
        if self.showing:
            self.show()

    def test(self):
        count = len(self.vertices)
        return pyglet.graphics.vertex_list(count, (self._vertex_type, self._raw_points), self.overlay.low_level(self))

    def set_overlay(self, overlay: _TemplateOverlay):
        self.overlay = overlay
        self.update()

    def moveTo(self):  # override in other templates
        pass

    def move(self):  # override in other templates
        pass

    def rotate(self):  # override determined by dimensions
        pass

    def _get_vertex_data(self, vertices: tuple, overlay: _TemplateOverlay):
        count = len(vertices) // self.dimension
        return count, self.mode, [i for i in range(count)], (self._vertex_type, vertices), overlay.low_level(self)

    def _points_to_raw(self, points: list):
        x = ()
        for pt in points:
            x += pt
        return x

    def _raw_to_points(self, raw_points: tuple):
        stuff = []
        raw_points = list(raw_points)
        while len(raw_points) > 0:
            stuff.append(tuple(raw_points[0:self.dimension]))
            raw_points = raw_points[self.dimension: len(raw_points)]
        return stuff

    def _get_vertex_list(self):
        return self._make_vertex_list(self._raw_points, self.overlay)

    def _make_vertex_list(self, vertices: tuple, overlay: _TemplateOverlay):
        if self.vertex_list is not None:
            self.vertex_list.delete()
        return self.group.add_raw(*self._get_vertex_data(vertices, overlay))

    def pair(self, other):  # can't type while in the class
        other.group.add(self)

    def unpair(self, other):
        self.group.remove(other)

    def __add__(self, other):
        self.pair(other)

    def __sub__(self, other):
        self.unpair(other)

    def hide(self):
        self.vertex_list.delete()
        self.vertex_list = self._get_vertex_list()

    def show(self):
        self.showing = True
        low.group.add(self)


# draw group  # todo make this better
class Group:
    def __init__(self, *args):
        self.type = None
        self.Batch3 = pyglet.graphics.Batch()
        self.Batch2 = pyglet.graphics.Batch()
        self.Batch4 = None
        self._2 = 0
        self._3 = 0
        for item in args:
            self.add(item)

    def render(self):
        if self._2 > 0:
            low.assert_2d()
            self.Batch2.draw()
        if self._3 > 0:
            low.enable_3d()
            self.Batch3.draw()

    def add_raw(self, count: int, mode, indices: list, position_data: tuple, overlay_data: tuple):
        dimension = int(position_data[0][1])
        if dimension == 2:
            self._2 += 1
            return self.Batch2.add_indexed(count, mode, None, indices, position_data,
                                           overlay_data)  # count, mode, group, indices, data
        elif dimension == 3:
            self._3 += 1
            return self.Batch3.add_indexed(count, mode, None, indices, position_data, overlay_data)
        else:
            pass

    def add(self, other: _ElementTemplate):
        vertex_list = other.vertex_list  # accessing may change
        if other.dimension == 2:
            other_batch = other.group.Batch2
            other_batch.migrate(vertex_list, other.mode, None, self.Batch2)  # vertex list, mode, group, batch
            self._2 += 1
        elif other.dimension == 3:
            other_batch = other.group.Batch3
            other_batch.migrate(vertex_list, other.mode, None, self.Batch3)  # vertex list, mode, group, batch
            self._3 += 1
        else:
            pass
        return vertex_list

    def remove(self, other: _ElementTemplate):
        vertex_list = other.vertex_list  # accessing may change
        if other.dimension == 2:
            other_batch = other.group.Batch2
            self.Batch2.migrate(vertex_list, other.mode, None, other_batch)  # vertex list, mode, group, batch
            self._2 -= 1
        elif other.dimension == 3:
            other_batch = other.group.Batch3
            self.Batch3.migrate(vertex_list, other.mode, None, other_batch)  # vertex list, mode, group, batch
            self._3 -= 1
        else:
            pass

    def __add__(self, other: _ElementTemplate):
        return self.add(other)

    def __sub__(self, other: _ElementTemplate):
        return self.remove(other)
