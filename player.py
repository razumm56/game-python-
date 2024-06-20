import pygame as pg
import numpy as np
from numba import njit
from raycasting import check_walls


class Player:
    def __init__(self, pressed_keys, pos_x, pos_y, rot, map_h, elapsed_time, rot_v):
        self._x = pos_x
        self._y = pos_y
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._diagonal = 0
        self._pressed_keys = pressed_keys
        self._map_h = map_h
        self._elapsed_time = elapsed_time
        if pg.mouse.get_focused():
            p_mouse = pg.mouse.get_rel()
            self._rot = rot + np.clip((p_mouse[0]) / 200, -0.2, .2)
            self._rot_v = rot_v + np.clip((p_mouse[1]) / 200, -0.2, .2)
            self._rot_v = np.clip(self._rot_v, -0.999, .999)

    def movement(self):
        speed = self._elapsed_time

        if self._pressed_keys[pg.K_LSHIFT] or self._pressed_keys[pg.K_RSHIFT]:
            speed *= 1.5

        if self._pressed_keys[pg.K_UP] or self._pressed_keys[ord('w')]:
            self._x += speed * np.cos(self._rot)
            self._y += speed * np.sin(self._rot)
            self._diagonal = 1

        elif self._pressed_keys[pg.K_DOWN] or self._pressed_keys[ord('s')]:
            self._x -= speed * np.cos(self._rot)
            self._y -= speed * np.sin(self._rot)
            self._diagonal = 1

        if self._pressed_keys[pg.K_LEFT] or self._pressed_keys[ord('a')]:
            speed /= (self._diagonal + 1)
            self._x += speed * np.sin(self._rot)
            self._y -= speed * np.cos(self._rot)

        elif self._pressed_keys[pg.K_RIGHT] or self._pressed_keys[ord('d')]:
            speed /= (self._diagonal + 1)
            self._x -= speed * np.sin(self._rot)
            self._y += speed * np.cos(self._rot)

        self._x, self._y = check_walls(self._pos_x, self._pos_y, self._map_h, self._x, self._y)

        return self._x, self._y, self._rot, self._rot_v



