################################################################################
# File: Target_animation.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Description: Tool to animate flies.
#              TO
#              DO             
################################################################################

import os
import pyglet
import cv2
from pyglet.gl import *
from random import *
from math import pi, sin, cos, atan2, sqrt

# Class: Target
# =============
class Target():
    def __init__(self, type, start, end, v, size):
        self.type = type
        self.start = start
        self.pos = start
        self.end = end
        self.v = v
        self.size = size

    def change_position(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def next_position(self):
        if self.type == 0:
            self.change_position(0, 0)
        elif self.type == 1:
            dx = randint(-self.v, self.v)
            dy = randint(-self.v, self.v)
            self.change_position(dx, dy)
        elif self.type == 2:
            x_c = self.end[0] - self.start[0]
            y_c = self.end[1] - self.start[1]
            deg = atan2(y_c, x_c)
            dx = 5.0 * cos(deg)
            dy = 5.0 * sin(deg)
            self.change_position(dx, dy)

# Class: AnimationWindow
# ======================
# This class is extension of Class pyglet.window.Window. It animates
# N flies flying in parallel. It is very hard coded.
class AnimationWindow(pyglet.window.Window):
    def __init__(self, target_list, directory):
        super(AnimationWindow, self).__init__()

        self.background = pyglet.image.load('test.jpg').get_texture()

        self.target_list = target_list
        self.N = len(target_list)
        self.time = 0
        self.directory = directory

    def circle(self, x, y, radius):
        glColor3f(0, 0, 0)
        iterations = int(2*radius*pi)
        s = sin(2*pi / iterations)
        c = cos(2*pi / iterations)
        dx, dy = radius, 0
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(iterations-5):
            glVertex2f(x+dx, y+dy)
            dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        glEnd()

    def update_frames(self, dt):
        for i in range(self.N):
            self.target_list[i].next_position()

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        glColor3f(1, 1, 1)
        self.background.blit(0, 0)
        for i in range(self.N):
            x = self.target_list[i].pos[0]
            y = self.target_list[i].pos[1]
            size = self.target_list[i].size
            self.circle(x, y, size)
        image_name = self.directory + "/scr" + str(self.time) + ".png"
        pyglet.image.get_buffer_manager().get_color_buffer().save(image_name)
        self.time += 1

# Class: FlyAnimation
# ===================
# This class contains different possible fly animation.
# Method run_random runs n flies randomly around the screen.
# Method run_parallel runs n flies in parallel through the screen.
class Animation():
    def __init__(self):
        self.target_list = []

    def add_target(self, type, start=[0, 0], end=[100, 100], v=5, size=10):
        new_target = Target(type, start, end, v, size)
        self.target_list.append(new_target)

    def make_directory(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            print "Making dir!"
            os.makedirs(directory)

    def create_movie(self):
        print "Hello!"
        img1 = cv2.imread('test/scr0.png')
        height, width, layers =  img1.shape
        print height, width, layers
        codec = 0
        video = cv2.VideoWriter('output.avi', codec, 20.0, (width,height))

        for i in range(30):
            img_name = "test/scr" + str(i) + ".png"
            print img_name
            img = cv2.imread(img_name)
            cv2.imshow("Frame", img)
            video.write(img)

        video.release()
        cv2.destroyAllWindows()

    def run(self, directory="test", fps=10):
        self.make_directory(directory)
        window = AnimationWindow(self.target_list, directory)
        pyglet.clock.schedule_interval(window.update_frames, 1.0/fps)
        pyglet.app.run()
        # Change this:
        print "I'm here"
        self.create_movie()


# Test
# ====
test = Animation()
test.add_target(2, start=[100,100], end=[500,500], size=8, v=10)
test.run()
