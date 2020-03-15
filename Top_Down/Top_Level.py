import pyglet
from Low_Level import LowLevel
import math
from pyglet.window.key import *
from Resources.Overlays import BLACK, Color
from Resources.Rendering import Group


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
        self.turn_sensivity = 10  # 1-100 = pixels mouse moves per degree of rotation
        self.mouse_locked = False
        self.key_checker = KeyStateHandler()
        self.push_handlers(self.key_checker)

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
        speed = 20
        if self.is_pressed(DOWN) or self.is_pressed(S):
            self.move_forward(-dt * speed)
        elif self.is_pressed(UP) or self.is_pressed(W):
            self.move_forward(dt * speed)
        elif self.is_pressed(RIGHT) or self.is_pressed(D):
            self.move_sideways(dt * speed)
        elif self.is_pressed(LEFT) or self.is_pressed(A):
            self.move_sideways(-dt * speed)
        self.render_shown()

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

    def render_shown(self):
        self.clear()
        self._inner.render()

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

    def set_background(self, color: Color):
        pyglet.gl.glClearColor(*color.raw())

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
        self._inner.update_camera_position()

    def move_sideways(self, dis):
        side, up = self.rotation
        side += 90
        dx = math.sin(math.radians(side)) * dis
        dz = math.cos(math.radians(side)) * dis
        dy = 0  # math.sin(math.radians(up)) * dis
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz
        self._inner.update_camera_position()

    def is_pressed(self, key):
        return self.key_checker[key]