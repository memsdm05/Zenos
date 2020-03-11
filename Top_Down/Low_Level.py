from pyglet.gl import *
from math import *
from Top_Down.Math import Vector2, Vector3


class LowLevel:
    width = None
    height = None

    def __init__(self, window):
        self.top_level = window
        self.mode = 2
        LowLevel.width, LowLevel.height = window.get_size()


    @staticmethod
    def convert_pos(pos):
        if len(pos) == 2:
            return Vector2(*pos)
        elif len(pos) == 3:
            return Vector3(*pos)

    def enable_3d(self):
        width, height = self.top_level.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.top_level.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.top_level.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, cos(radians(x)), 0, sin(radians(x)))
        x, y, z = self.top_level.position
        glTranslatef(-x, -y, -z)
        self.mode = 3

    def enable_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.mode = 2

    def assert_3d(self):
        if self.mode != 3:
            self.enable_3d()

    def assert_2d(self):
        if self.mode != 2:
            self.enable_2d()
