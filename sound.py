import pygame as pg
import settings


class Sound:
    def __init__(self):
        self._sound = {}

    def load_sounds(self):
        self._sound['step'] = pg.mixer.Sound('Assets/Sounds/playerstep.mp3')
        self._sound['step2'] = pg.mixer.Sound('Assets/Sounds/enemystep.mp3')
        self._sound['swoosh'] = pg.mixer.Sound('Assets/Sounds/sword.mp3')
        self._sound['swoosh2'] = pg.mixer.Sound('Assets/Sounds/sword2.mp3')
        self._sound['shot'] = pg.mixer.Sound('Assets/Sounds/gun.mp3')
        self._sound['shot2'] = pg.mixer.Sound('Assets/Sounds/gun2.mp3')
        self._sound['hurt'] = pg.mixer.Sound('Assets/Sounds/damage.mp3')
        self._sound['deadmonster'] = pg.mixer.Sound('Assets/Sounds/deadmonster.mp3')
        self._sound['hitmonster'] = pg.mixer.Sound('Assets/Sounds/hitmonster.mp3')
        self._sound['hitmonster2'] = pg.mixer.Sound('Assets/Sounds/hitmonster2.mp3')
        self._sound['healthup'] = pg.mixer.Sound('Assets/Sounds/healthup.wav')
        self._sound['died'] = pg.mixer.Sound('Assets/Sounds/Y2mate.mx - Dark Souls death screen - HD (128 kbps).mp3')
        self._sound['won'] = pg.mixer.Sound('Assets/Sounds/won.wav')
        self._sound['music0'] = pg.mixer.Sound('Assets/Sounds/Тема для меню. (promodj.com).mp3')
        self._sound['music1'] = pg.mixer.Sound('Assets/Sounds/win.mp3')
        self._sound['music2'] = pg.mixer.Sound('Assets/Sounds/Y2mate.mx - Doom Eternal OST - The Only Thing They Fear Is You (Mick Gordon) [Doom Eternal Theme] (128 kbps).mp3')
        self._sound['music3'] = pg.mixer.Sound('Assets/Sounds/omega_droid-airborne_with_wind.wav')
        self._sound['music4'] = pg.mixer.Sound('Assets/Sounds/Flaming Soul.mp3')
        self._sound['music5'] = pg.mixer.Sound('Assets/Sounds/Y2mate.mx - Attack on titan- battle theme (128 kbps).mp3')
        self._sound['music6'] = pg.mixer.Sound('Assets/Sounds/OMFG - Hello _ METAL REMIX by Vincent Moretto.mp3')
        return self._sound

    def set_volume(self, m_vol, sfx_vol):
        for key in self._sound.keys():
            self._sound[key].set_volume(sfx_vol)
        for i in range(7):  # изменение громкости музыки
            self._sound[f'music{i}'].set_volume(m_vol)