import pygame as pg
from settings import *
from menu import Menu

Menu = Menu()


class Texture:
    def __init__(self):
        self.map = {}
        self.ui = {}

    def load_textures_map(self, textures):
        self.map['sky1'] = pg.image.load('Assets/Textures/skybox' + str(textures[0]) + '.jpg')
        self.map['floor'] = pg.surfarray.array3d(pg.image.load('Assets/Textures/floor' + str(textures[1]) + '.jpg'))  # /255
        self.map['wall'] = pg.surfarray.array3d(pg.image.load('Assets/Textures/wall' + str(textures[2]) + '.jpg'))  # /255
        self.map['b_wall'] = pg.transform.smoothscale(pg.image.load('Assets/Textures/wall' + str(textures[2]) + '.jpg'), (25, 25))
        self.map['b_wall'] = pg.surfarray.array3d(pg.transform.smoothscale(self.map['b_wall'], (100, 100)))  # /255
        self.map['door'] = pg.surfarray.array3d(pg.image.load('Assets/Textures/door' + str(textures[3]) + '.jpg'))  # /255
        self.map['window'] = pg.surfarray.array3d(pg.image.load('Assets/Textures/window' + str(textures[4]) + '.jpg'))  # /255
        self.map['blood'] = pg.image.load('Assets/Textures/blood0.png')
        self.map['blood_size'] = np.asarray(self.map['blood'].get_size())
        if textures[0] % 3 > 0:
            self.map['floor'] = (self.map['floor'] * (1 - 0.2 * textures[0] % 3)).astype(int)
            self.map['wall'] = (self.map['wall'] * (1 - 0.2 * textures[0] % 3)).astype(int)
            self.map['b_wall'] = (self.map['b_wall'] * (1 - 0.2 * textures[0] % 3)).astype(int)
            self.map['door'] = (self.map['door'] * (1 - 0.2 * textures[0] % 3)).astype(int)
            self.map['window'] = (self.map['window']* (1 - 0.2 * textures[0] % 3)).astype(int)

        return self.map

    def load_texture_ui(self, clock, font, screen):
        self.ui['menu'] = [pg.image.load('Assets/Textures/menu0.png').convert_alpha()]
        self.ui['menu'].append(pg.image.load('Assets/Textures/options.png').convert_alpha())
        self.ui['menu'].append(pg.image.load('Assets/Textures/credits.png').convert_alpha())
        self.ui['menu'].append(pg.image.load('Assets/Textures/menu1.png').convert_alpha())
        self.ui['hearts'] = pg.image.load('Assets/Textures/hearts.png').convert_alpha()
        self.ui['colonel'] = pg.image.load('Assets/Sprites/colonel1.png').convert_alpha()
        self.ui['hearts2'] = pg.Surface.subsurface(self.ui['hearts'], (0, 0, player_health * 10, 20))
        self.ui['exit1'] = pg.image.load('Assets/Textures/exit.png').convert_alpha()
        self.ui['exits'] = [pg.Surface.subsurface(self.ui['exit1'], (0, 0, 50, 50)),
                            pg.Surface.subsurface(self.ui['exit1'], (50, 0, 50, 50))]
        self.ui['splash'] = []
        for i in range(4):
            self.ui['splash'].append(pg.image.load('Assets/Textures/splash' + str(i) + '.jpg').convert())

        self.ui['sky1'] = self.ui['hearts'].copy()
        self.ui['msg'] = "Press any key..."
        self.ui['surf'] = self.ui['splash'][0].copy()
        Menu.splash_screen(self.ui['msg'], self.ui['splash'][0], clock, font, screen)
        self.ui['msg'] = " "
        return self.ui


