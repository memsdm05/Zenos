from pyglet.gl import *
from math import *
from Top_Down.Resources.Math import Vector


class LowLevel:
    width = None
    height = None
    active = None

    def __init__(self, window):
        self.top_level = window
        self.mode = 2
        LowLevel.width, LowLevel.height = window.get_size()
        LowLevel.active = self

    @staticmethod
    def convert_pos(pos):
        if len(pos) == 3:
            x, y, z = pos
            return Vector(-x, y, z)
        return Vector(*pos)

    def enable_3d(self):
        # self.top_level.Projection()
        width, height = self.top_level.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.top_level.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70.0, width / float(height), 0.1, 1000.0)  # FOVy, window dimensions, near, far range of view
        glMatrixMode(GL_MODELVIEW)
        self.update_camera_position()
        self.mode = 3

    def update_camera_position(self):
        glLoadIdentity()  # not sure what this does
        x, y = self.top_level.rotation  # retrieve x (sideways turn), and y (updown turn)
        glRotatef(x + 180, 0, 1, 0)  # turn camera to face side direction (for some reason 0 = face neg)
        glRotatef(y, cos(radians(x)), 0, sin(radians(x)))  # rotate up down
        x, y, z = self.top_level.position  # retrieve camera position
        glTranslatef(x, -y, -z)  # move the camera

    def enable_2d(self):
        width, height = self.top_level.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.top_level.get_viewport_size()
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
