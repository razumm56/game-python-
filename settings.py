import numpy as np
import moviepy.editor
import pygame as pg


#game settings
WIDTH = 800
HEIGHT = 600
running = 1
pause = 1
options = 0
newgame = 2
timer = 0
hres = max(min(250, 800), 80)
halfvres = int(hres * 0.375)
mod = hres / 60
frame = np.random.randint(0, 255, (hres, halfvres * 2, 3))
exit_2 = 1

#window
fullscreen = 0
level = 0
player_health = 0
current_sword_sprite = 0
story = 0
#level
# sky1, floor, wall, door, window, enemies
level_textures = [[0, 1, 0, 0, 1, 3],  # level 0
                  [0, 2, 1, 1, 0, 1],  # level 1
                  [1, 0, 2, 1, 1, 2],  # level 2
                  [1, 3, 1, 0, 0, 0],  # level 3
                  [2, 1, 2, 1, 1, 4],  # level 4
                  [2, 0, 0, 0, 0, 5]]  # level 5


step_delay = pg.time.get_ticks() / 200
step_delay2 = step_delay
click, click_delay = 0, step_delay

# SOUND
m_vol = 0.1
sfx_vol= 0.1
music = 0

#video
video = moviepy.editor.VideoFileClip("./Assets/Textures/video.mp4")

