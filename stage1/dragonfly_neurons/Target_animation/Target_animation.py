################################################################################
# File: Target_animation.py
# Author: Erik Grabljevec
# E-mail: erikgrabljevec5@gmail.com
# Doc: Tool to animate flies. As user only interect with class Animation
#      To create new animation create new instance of class Animation.
#      Animation has next methods (each followed with list of arguments):
#
#       add_target: 
#                - type : it is either 0 for stationary target,
#                         1 for randomly moving target and 2 for target
#                         moving from start to end.
#                - start = [0, 0] : starting position.
#                - end = [100, 100] : ending position, only relavant for type 2.
#                - v = 5 : sets velocity of target.
#                - size = 10 : sets size of target.
#                - color = [0, 0, 0]) : sets color of target.
#              
#       add_background: 
#                - img_dir = False : sets directory of background image.
#                                    If it stays False background is white.
#                - speed = 0 : sets how fast the background is moving.
#
#       run:
#                - out_directory : sets directory+name of output movie.
#                - fps = 10 : sets fps used to make animation.
################################################################################

import os
import pyglet
from pyglet.gl import *
import cv2
from random import *
from math import pi, sin, cos, atan2, sqrt


# Class: Target
# =============
# This class represents different targets that will move on the screen.
# (Refer to top of the file).
class Target:
    def __init__(self, type, start, end, v, size, color):
        self.type = type
        self.start = start
        self.pos = start
        self.end = end
        self.v = v
        self.size = size
        self.color = color

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
            dx = self.v * cos(deg)
            dy = self.v * sin(deg)
            self.change_position(dx, dy)

# Class: AnimationWindow
# ======================
# This class is extension of Class pyglet.window.Window. It animates
# N flies flying in parallel. It is very hard coded.
# (Refer to top of the file).
class AnimationWindow(pyglet.window.Window):
    def __init__(self, target_list, width, height, bg_image, bg_speed):
        super(AnimationWindow, self).__init__()
        
        self.bg_image = bg_image
        if self.bg_image:
            self.bg_speed = bg_speed
            self.background = pyglet.image.load(self.bg_image).get_texture()
            
        self.target_list = target_list
        self.N = len(target_list)
        self.time = 0

    def circle(self, x, y, radius, color):
        glColor3f(color[0], color[1], color[2])
        iterations = int(2*radius*pi)+15
        s = sin(2*pi / iterations)
        c = cos(2*pi / iterations)
        dx, dy = radius, 0
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(iterations):
            glVertex2f(x+dx, y+dy)
            dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        glEnd()

    def update_frames(self, dt):
        for i in range(self.N):
            self.target_list[i].next_position()

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        if self.bg_image:
            glColor3f(1, 1, 1)
            bg_pos = -self.time * self.bg_speed
            self.background.blit(bg_pos, bg_pos)
        for i in range(self.N):
            x = self.target_list[i].pos[0]
            y = self.target_list[i].pos[1]
            size = self.target_list[i].size
            color = self.target_list[i].color
            self.circle(x, y, size, color)
        image_name = "temp/scr" + str(self.time) + ".png"
        pyglet.image.get_buffer_manager().get_color_buffer().save(image_name)
        self.time += 1

# Class: FlyAnimation
# ===================
# This class contains different possible fly animation.
# Method run_random runs n flies randomly around the screen.
# Method run_parallel runs n flies in parallel through the screen.
# (Refer to top of the file).
class Animation:
    def __init__(self, width=640, height=480):
        self.target_list = []
        self.width = width
        self.height = height

    def make_directory(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_movie(self, out_directory, total_frames):
        img1 = cv2.imread('temp/scr0.png')
        height, width, layers =  img1.shape
        codec = cv2.cv.CV_FOURCC('M','J','P','G')
        print out_directory
        video = cv2.VideoWriter(out_directory, codec, 20.0, (width,height))

        for i in range(total_frames):
            img_name = "temp/scr" + str(i) + ".png"
            img = cv2.imread(img_name)
            video.write(img)

        video.release()
        cv2.destroyAllWindows()

    def add_target(self, type, start=[0, 0], end=[100, 100], 
                   v=5, size=10, color=[0, 0, 0]):
        new_target = Target(type, start, end, v, size, color)
        self.target_list.append(new_target)
        
    def add_background(self, img_dir=False, speed=0):
        self.bg_image = img_dir
        self.bg_speed = speed

    def run(self, out_directory, fps=10, total_frames=50):
        self.make_directory("temp")
        window = AnimationWindow(self.target_list, self.width, self.height, 
                                 self.bg_image, self.bg_speed)
        pyglet.clock.schedule_interval(window.update_frames, 1.0/fps)
        pyglet.app.run()
        self.create_movie(out_directory, total_frames)
        
