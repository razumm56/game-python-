import pygame as pg
import numpy as np
from numba import njit
from settings import *
from player import Player
from sound import Sound
from texture import *
from menu import Menu
from map import Map
from sprites import *
from raycasting import *
from drawing import Draw
from texture import Texture
import json
import datetime


Game_map = Map()
Sound = Sound()
Menu = Menu()
Sprites = Sprites()
Draw = Draw()
Texture = Texture()

pg.init()
# верхняя панель
pg.display.set_caption("Dead and - A Python game by razumm, thanks for playing!")
font = pg.font.SysFont("Courier New", 70)

# загрузка мелодии меню
sounds = Sound.load_sounds()
Sound.set_volume(m_vol, sfx_vol)
sounds['music' + str(music)].play(-1)

# обработка тиков
step_delay = pg.time.get_ticks() / 200
step_delay2 = step_delay
click, click_delay = 0, step_delay

# разрешение экрана
screen = pg.display.set_mode((WIDTH, HEIGHT))

# курсор и время
clock = pg.time.Clock()
pg.mouse.set_visible(False)
pg.event.set_grab(True)

# load ui
ui = Texture.load_texture_ui(clock, font, screen)

'''Функиця для добавление времени в json файл'''
def add_time_list(timer):
    my_data_time = datetime.datetime.now()
    data_string = my_data_time.strftime("%Y-%m-%d %H:%M:%S")
    data_to_save = {data_string: round(timer, 1)}
    with open('best_times.json', 'r+') as file:
        file_data = json.load(file)
        file_data["passage_times"].append(data_to_save)
        file.seek(0)
        json.dump(file_data, file, indent=4)
'''----------------------------------------------------------'''

while running:
    '''----------- Инициализация игры, проверка здоровья и уровней------------------'''
    pg.display.update()
    ticks = pg.time.get_ticks() / 200
    elapsed_time_limit = min(clock.tick() / 500, 0.3)
    if not pause and (player_health <= 0 or (exit_2 == 0 and int(pos_x) == exit_x and int(pos_y) == exit_y)):
        msg = ' '
        if player_health <= 0:
            sounds['died'].play()
            video.preview()
            newgame = 2
            surface = ui['splash'][3].copy()
        else:
            level += 1
            player_health = min(player_health + 2, 20)
            sounds['won'].play()
            newgame = 1
            if level > 5:
                level, newgame = 0, 2
                sounds['died'].play()
                surface = ui['splash'][2].copy()
                surface.blit(font.render('Total time: ' + str(round(timer, 1)), 1, (255, 255, 255)), (20, 525))
                add_time_list(timer)
            else:
                msg = "Cleared level " + str(level - 1) + '!'
        Menu.splash_screen(msg, surface, clock, font, screen)
        pause, click_delay = 1, ticks
        pg.time.wait(500)
        '''---------------------------------------------------------------------------------------------------'''

    '''-----------------Обработка вспомогательных кнопок интерфейса---------------------'''
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if current_sword_sprite < 1 and not pause:
                current_sword_sprite = 1
            if pause and ticks - click_delay > 1:
                click, click_delay = 1, ticks
                sounds['healthup'].play()

        if event.type == pg.KEYDOWN:
            if event.key == ord('p') or event.key == pg.K_ESCAPE:
                if not pause:
                    pause = 1
                else:
                    if options > 0:
                        options = 0
                    elif newgame == 0:
                        pause = 0
                pg.mouse.set_pos(400, 300)

            if event.key == ord('f'):  # toggle fullscreen
                pg.display.toggle_fullscreen()
                fullscreen = not (fullscreen)
    '''-------------------------------------------------------------------------------------'''

    '''---------------------------Обработка интерфейса, загрузка или генерация уровня---------------------------'''
    if pause:
        clock.tick(60)
        surface_2, pause, options, running, newgame, adjust_res, m_vol, sfx_vol, story = Menu.pause_menu(
            ui['surf'].copy(), ui['menu'], pause, options, click, running, m_vol, sfx_vol, Sound, newgame, font,
            ui['msg'], level,
            ticks, hres, story)

        if adjust_res != 1:
            hres, halfvres, mod, frame = Menu.adjust_resolution(int(hres * adjust_res))
            sky = pg.surfarray.array3d(pg.transform.smoothscale(ui['sky1'], (720, halfvres * 4)))  # /255
            adjust_res = 1

        screen.blit(surface_2, (0, 0))
        click = 0

        if newgame == 1:
            newgame, pause = 0, not (pause)
            if player_health <= 0 or msg[0] != 'C':
                surface = ui['splash'][1].copy()
                Menu.splash_screen(' ', surface, clock, font, screen)
                level, player_health, timer = 0, 20, -0.1

            if np.random.randint(0, 7) != music:
                sounds['music' + str(music)].fadeout(1000)
                music = np.random.randint(1, 7)
                sounds['music' + str(music)].play(-1)

            msg = 'Loading...'
            surface_2 = surface.copy()
            surface_2.blit(font.render(msg, 1, (255, 255, 255)), (30, 500))
            surface_2.blit(font.render(msg, 1, (30, 255, 155)), (32, 502))
            screen.blit(surface_2, (0, 0))
            pg.display.update()
            msg = 'Kill the monsters!'

            if story:
                pos_x, pos_y, rot, rot_v, map_height, map_color, exit_x, exit_y, step_count, size = Map.load_map(level)
                number_level = level_textures[level]

            else:
                size = np.random.randint(10 + level * 2, 16 + level * 2)
                number_enemies = size
                pos_x, pos_y, rot, rot_v, map_height, map_color, exit_x, exit_y, step_count = Map.generate_map(size)
                number_level = [np.random.randint(0, 3),  # sky1
                          np.random.randint(0, 4),  # floorwall
                          np.random.randint(0, 3),  # wall
                          np.random.randint(0, 2),  # door
                          np.random.randint(0, 2),  # window
                          np.random.randint(0, 5),  # enemies
                          ]
            number_enemies = level ** 2 + 10 - level
            sprites, sprite_size, sword, current_sword_sprite, select_weapon = Sprites.get_sprites(number_level[5])
            textures_map = Texture.load_textures_map(number_level)
            sky = pg.surfarray.array3d(pg.transform.smoothscale(textures_map['sky1'], (720, halfvres * 4)))
            enemies = Sprites.spawn_enemies(number_enemies, map_height, size, pos_x, pos_y, level / 2)
            hearts_2 = pg.Surface.subsurface(ui['hearts'], (0, 0, player_health * 10, 20))
            exit_2, damage_mod, blood_scale = 1, 1, 1
            enemies_heatmap, mini_map = np.zeros((size, size)), np.zeros((size, size, 3))
            sounds['healthup'].play()
        '''----------------------------------------------------------------------------------------------'''

        '''------------Отрисовка: кадра игры, спрайтов, элементов интерфейса, добавление звуков------------'''
    else:
        timer = timer + elapsed_time_limit / 2
        frame = new_frame(pos_x - 0.2 * np.cos(rot), pos_y - 0.2 * np.sin(rot), rot, frame, sky, textures_map['floor'],
                          hres, halfvres, mod, map_height, size, textures_map['wall'], map_color, exit_x, exit_y,
                          rot_v, textures_map['door'], textures_map['window'], textures_map['b_wall'], exit_2)
        surface = pg.surfarray.make_surface(frame)

        enemies_heatmap = np.zeros((size, size))
        health = player_health
        enemies, player_health, enemies_heatmap = enemies_ai(pos_x, pos_y, enemies, map_height, size, enemies_heatmap,
                                                   current_sword_sprite, ticks, player_health, number_enemies, level / 3)
        enemies = sort_sprites(pos_x - 0.2 * np.cos(rot), pos_y - 0.2 * np.sin(rot), rot, enemies, map_height, size,
                               elapsed_time_limit / 3, select_weapon)
        if exit_2 == 0:
            surface = Draw.draw_colonel(surface, ui['colonel'], pos_x - 0.2 * np.cos(rot), pos_y - 0.2 * np.sin(rot),
                                        exit_x + 0.5, exit_y + 0.5, hres, halfvres, rot, rot_v, map_height, size)

        surface, enemies_index = Draw.draw_sprites(surface, sprites, enemies, sprite_size, hres, halfvres, ticks,
                                     sword, current_sword_sprite, rot_v)

        if int(current_sword_sprite) > 0 and damage_mod < 1 and select_weapon == 1:
            blood_scale = blood_scale * (1 + elapsed_time_limit)
            scaled_blood = pg.transform.scale(textures_map['blood'], 4 * blood_scale *
                                              textures_map['blood_size'] * hres / 800)
            surface.blit(scaled_blood, np.asarray([hres/2, halfvres]) - 2 *
                         blood_scale * textures_map['blood_size'] * hres / 800)

        surface = pg.transform.scale2x(surface)
        surface = pg.transform.smoothscale(surface, (800, 600))
        surface.blit(hearts_2, (20, 20))

        if exit_2 == 0:
            mini_map[int(pos_x)][int(pos_y)] = (50, 50, 255)
            surface_map = pg.surfarray.make_surface(mini_map.astype('uint8'))
            surface_map = pg.transform.scale(surface_map, (size * 5, size * 5))
            surface.blit(surface_map, (20, 50), special_flags=pg.BLEND_ADD)
            mini_map[int(pos_x)][int(pos_y)] = (100, 100, 0)

        surface.blit(font.render(str(round(timer, 1)), 1, (255, 255, 255)), (20, 525))
        surface.blit(font.render(str(round(number_enemies, 1)), 1, (255, 0, 0)), (700, 525))
        surface.blit(ui['exits'][exit_2], (730, 20))
        screen.blit(surface, (0, 0))

        if health > player_health:
            hearts_2 = pg.Surface.subsurface(ui['hearts'], (0, 0, player_health * 10, 20))
            sounds['hurt'].play()

        if ticks - step_delay > 2 and step_count != pos_x + pos_y:
            sounds['step'].play()
            step_delay = ticks
        step_count = pos_x + pos_y

        if enemies_heatmap[int(pos_x)][int(pos_y)] > 0:
            delay_control = max(0.3, 2 / np.random.uniform(0.99, enemies_heatmap[int(pos_x)][int(pos_y)]))
            if ticks - step_delay2 > delay_control:
                sounds['step2'].play()
                step_delay2 = ticks

        '''-------------------------------------------------------------------------------------------------------'''
        '''--------------------------------------Механика стрельбы и удара мечом-----------------------------------'''
        if int(current_sword_sprite) > 0:
            if current_sword_sprite == 1:
                damage_mod = 1
                if select_weapon == 0:
                    while 1 < enemies[enemies_index][3] < 10 and damage_mod > 0.1:
                        enemies[enemies_index][8] = enemies[enemies_index][8] - np.random.uniform(1, 4)
                        enemies[enemies_index][10] = ticks
                        x = enemies[enemies_index][0] + 0.3 * np.cos(rot)
                        y = enemies[enemies_index][1] + 0.3 * np.sin(rot)
                        if map_height[int(x)][int(y)] == 0:
                            enemies[enemies_index][0] = (x + enemies[enemies_index][0]) / 2  # push back
                            enemies[enemies_index][1] = (y + enemies[enemies_index][1]) / 2
                        if damage_mod == 1:
                            sounds['swoosh'].play()
                            if enemies[enemies_index][4]:
                                sounds['hitmonster2'].play()
                            else:
                                sounds['hitmonster'].play()
                        damage_mod = damage_mod * 0.7
                        if enemies[enemies_index][8] < 0:
                            sounds['deadmonster'].play()
                            number_enemies = number_enemies - 1
                            if number_enemies == 0:
                                exit_2, msg = 0, "Find the master!"
                            if np.random.uniform(0, 1) < 0.3:
                                player_health = min(player_health + 0.5, 20)
                                hearts2 = pg.Surface.subsurface(ui['hearts'], (0, 0, player_health * 10, 20))
                                sounds['healthup'].play()
                        enemies_index = enemies_index - 1
                else:
                    while enemies[enemies_index][3] < 10 and damage_mod > 0.1 and enemies_index >= 0:
                        x = pos_x - 0.2 * np.cos(rot) + np.cos(rot + np.random.uniform(0, 0.05)) / enemies[enemies_index][3]
                        y = pos_y - 0.2 * np.sin(rot) + np.sin(rot + np.random.uniform(0, 0.05)) / enemies[enemies_index][3]
                        z = 0.5 + np.sin(rot_v * -0.392699) / enemies[enemies_index][3]
                        dist2en = np.sqrt((enemies[enemies_index][0] - x) ** 2 + (enemies[enemies_index][1] - y) ** 2)
                        if dist2en < 0.1 and z > 0 and z < 0.07 * enemies[enemies_index][5]:
                            if z > 0.05 * enemies[enemies_index][5]:
                                enemies[enemies_index][8] = enemies[enemies_index][8] - np.random.uniform(1, 2) * 2
                            else:
                                enemies[enemies_index][8] = enemies[enemies_index][8] - np.random.uniform(1, 2)
                            enemies[enemies_index][10] = ticks
                            x = enemies[enemies_index][0] + 0.3 * np.cos(rot)
                            y = enemies[enemies_index][1] + 0.3 * np.sin(rot)
                            if map_height[int(x)][int(y)] == 0:
                                enemies[enemies_index][0] = (x + enemies[enemies_index][0]) / 2  # push back
                                enemies[enemies_index][1] = (y + enemies[enemies_index][1]) / 2
                            if damage_mod == 1:
                                blood_scale = enemies[enemies_index][3]
                                sounds['shot'].play()
                                if enemies[enemies_index][4]:
                                    sounds['hitmonster2'].play()
                                else:
                                    sounds['hitmonster'].play()
                            damage_mod = damage_mod * 0.7
                            if enemies[enemies_index][8] < 0:
                                sounds['deadmonster'].play()
                                number_enemies = number_enemies - 1
                                if number_enemies == 0:
                                    exit_2, msg = 0, "Find the master!"
                                if np.random.uniform(0, 1) < 0.3:
                                    player_health = min(player_health + 0.5, 20)
                                    hearts2 = pg.Surface.subsurface(ui['hearts'], (0, 0, player_health * 10, 20))
                                    sounds['healthup'].play()

                        enemies_index = enemies_index - 1

                if damage_mod == 1:
                    if select_weapon == 0:
                        sounds['swoosh2'].play()
                    else:
                        sounds['shot2'].play()

            if select_weapon == 0:
                current_sword_sprite = (current_sword_sprite + elapsed_time_limit * 5) % 4
            else:
                current_sword_sprite = (current_sword_sprite + elapsed_time_limit * 3) % 4

        '''------------------------------------------------------------------------------------------'''

        fps = int(clock.get_fps())
        pg.display.set_caption(
            "Health: " + str(round(player_health, 1)) + " Enemies: " + str(number_enemies) + " FPS: " + str(
                fps) + ' ' + msg)
        player = Player(pg.key.get_pressed(), pos_x, pos_y, rot, map_height, elapsed_time_limit, rot_v)
        pos_x, pos_y, rot, rot_v = player.movement()


pg.mixer.fadeout(1000)
pg.time.wait(1000)
pg.quit()
