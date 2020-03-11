import pyglet
from Low_Level import LowLevel
import Resources


class Window(pyglet.window.Window):
    active_window = None

    def __init__(self):
        super(Window, self).__init__()
        self.rotation = 0
        self.position = 0, 0, 0
        self.mode = 2
        self.bg_color = Resources.BLACK
        Window.active_window = self
        self._inner = LowLevel(self)
        self._draw_items2 = []
        self._draw_items3 = []

    def start(self):
        pyglet.clock.schedule_interval(self._periodic, 1 / 120.0)
        pyglet.app.run()

    def quit(self):
        pass

    @staticmethod
    def _periodic(dt):
        Window.active_window.periodic(dt)

    def periodic(self, dt):
        pass

    def render(self, item):
        try:
            if item.type == 2:
                self._inner.assert_2d()
                item.render()
            elif item.type == 3:
                self._inner.assert_3d()
                item.render()
            elif type(item) == Resources.Group:
                item.render()
            else:
                print(f"**invalid item rendered: {item}")
                quit()
        except NameError:
            print("The item you tried to render was not valid")
            quit()

    def draw_all(self):
        self._inner.assert_2d()
        for item in self._draw_items2:
            item.render()
        self._inner.enable_3d()
        for item in self._draw_items3:
            item.render()

    def set_background(self, template):
        if type(template) is Resources.Color:
            pyglet.gl.glClearColor(*template.raw())