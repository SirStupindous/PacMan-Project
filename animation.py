from settings import *
import pygame as pg


class Animator(object):
    def __init__(self, frames=[], speed=20, loop=True):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False

    def reset(self):
        self.current_frame = 0
        self.finished = False

    def update(self, dt):
        if not self.finished:
            self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                self.current_frame -= 1

        return self.frames[self.current_frame]

    def nextFrame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0


class PortalTimer:
    def __init__(self, image_list, start_index=0, delay=100, is_loop=True):
        self.image_list = image_list
        self.delay = delay
        self.is_loop = is_loop
        self.last_time_switched = pg.time.get_ticks()
        self.frames = len(image_list)
        self.start_index = start_index
        self.index = start_index if start_index < len(image_list) - 1 else 0

    def next_frame(self):
        if self.is_expired():
            return
        now = pg.time.get_ticks()
        if now - self.last_time_switched > self.delay:
            self.index += 1
            if self.is_loop:
                self.index %= self.frames
            self.last_time_switched = now

    def reset(self):
        self.index = (
            self.start_index if self.start_index < len(self.image_list) - 1 else 0
        )

    def is_expired(self):
        return not self.is_loop and self.index >= len(self.image_list) - 1

    def image(self):
        self.next_frame()
        return self.image_list[self.index]
