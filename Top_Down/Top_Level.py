import pyglet
from Top_Down.Low_Level import LowLevel
import math
from pyglet.window.key import *
from Top_Down.Resources.Overlays import BLACK
from Top_Down.Resources.Rendering import Group


class Window(pyglet.window.Window):
    active_window = None
    keys = pyglet.window.key

    def __init__(self):
        super(Window, self).__init__()
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        self.rotation = 0, 0
        self.position = 0, 0, 0
        self.mode = 2
        self.bg_color = BLACK
        Window.active_window = self
        self._inner = LowLevel(self)
        self._draw_items2 = []
        self._draw_items3 = []
        self.turn_sensivity = 10  # 1-100 = pixels mouse moves per degree of rotation
        self.mouse_locked = False

    def start(self):
        pyglet.clock.schedule_interval(self._periodic, 1 / 120.0)
        pyglet.app.run()

    def quit(self):
        pyglet.app.exit()
        # quit()

    @staticmethod
    def _periodic(dt: float):
        Window.active_window.periodic(dt)

    def periodic(self, dt: float):
        pass

    def render(self, *args):
        for item in args:
            try:
                if type(item) == Group:
                    item.render()
                elif item.dimension == 2:
                    self._inner.assert_2d()
                    item.render()
                elif item.dimension == 3:
                    self._inner.assert_3d()
                    item.render()
                else:
                    print(f"**invalid item rendered: {item}")
                    quit()
            except NameError:
                print("The item you tried to render was not valid")
                self.quit()

    def draw_all(self):
        self._inner.assert_2d()
        for item in self._draw_items2:
            item.render()
        self._inner.enable_3d()
        for item in self._draw_items3:
            item.render()

    def on_mouse_motion(self, x, y, dx, dy):  # default will be altering camera view
        if self.mouse_locked:
            side, up = self.rotation
            theta_y = dy * self.turn_sensivity/100
            theta_x = dx * self.turn_sensivity/100
            self.rotation = side + theta_x, up + theta_y
            self._inner.update_camera_position()

    def on_key_press(self, symbol, modifiers):
        if symbol == DOWN:
            self.move_forward(-1)
        elif symbol == UP:
            self.move_forward(1)
        elif symbol == RIGHT:
            self.move_sideways(1)
        elif symbol == LEFT:
            self.move_sideways(-1)

    def set_background(self, template):
        pyglet.gl.glClearColor(*template.raw())

    def lock_mouse(self, should=True):  # todo add a escape
        self.mouse_locked = should
        self.set_exclusive_mouse(should)

    def move_forward(self, dis):
        side, up = self.rotation
        dx = math.sin(math.radians(side)) * dis
        dz = math.cos(math.radians(side)) * dis
        dy = math.sin(math.radians(up)) * dis
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz
        # self._inner.update_camera_position()
        self._inner.enable_3d()

    def move_sideways(self, dis):
        side, up = self.rotation
        side += 90
        dx = math.sin(math.radians(side)) * dis
        dz = math.cos(math.radians(side)) * dis
        dy = 0  # math.sin(math.radians(up)) * dis
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz
        # self._inner.update_camera_position()
        self._inner.enable_3d()