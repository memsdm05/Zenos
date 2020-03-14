from Top_Down.Zenos_package import *


class TestWindow(Window):
    c = ThreeD.Cube((2, 3, 10), 1, RED)

    def __init__(self):
        super(TestWindow, self).__init__()
        self.sky = TwoD.Rectangle((0, self.height), self.width, self.height//2, LIGHT_BLUE)
        self.ground = TwoD.Rectangle((0, self.height // 2), self.width, self.height // 2, BROWN)

    def periodic(self, dt):
        self.clear()
        self.render(self.sky, self.ground, self.c)
        x, y, z = self.position
        if y > 0:
            y -= dt
        if y < 0:
            y = 0
        self.position = x, y, z
        self._inner.enable_3d()
        # print(self.position)

    def on_key_press(self, symbol, modifiers):
        x, y, z = self.position
        if symbol == self.keys.DOWN:
            self.position = x, y, z-1
        if symbol == self.keys.UP:
            self.position = x, y, z+1
        if symbol == self.keys.LEFT:
            self.position = x-1, y, z
        if symbol == self.keys.RIGHT:
            self.position = x+1, y, z
        if symbol == self.keys.SPACE:
            self.position = x, y+10, z


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(Resources.LIGHT_BLUE)
    x.lock_mouse()
    x.start()