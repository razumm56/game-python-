from numba import njit
import pygame as pg
import numpy as np
from raycasting import *


class Sprites:
    def __init__(self):
        self.enemies = []
        self.sword_sprites = []
        self.enemy_sprites = [[], []]

    def spawn_enemies(self, number_enemies, map_height, size, pos_x, pos_y, level=0):
        self.enemies = []
        for i in range(number_enemies):
            x, y = np.random.randint(1, size - 2), np.random.randint(1, size - 2)
            while map_height[x][y] or (x == int(pos_x) and y == int(pos_y)):
                x, y = np.random.randint(1, size - 2), np.random.randint(1, size - 2)
            x, y = x + 0.5, y + 0.5
            player_angle, player_inv_dist, player_direction = 0, 1, 0
            enemyType = np.random.choice([0, 1])  # 0 вид врагов
            enemy_facing_direction = np.random.uniform(0, 2 * np.pi)  # угол поворота
            size = np.random.uniform(7, 10)
            health = size / 2 + level / 3
            state = np.random.randint(0, 3)  # 0 normal, 1 aggressive, 2 defensive
            cooldown = 0
            self.enemies.append([x, y, player_angle, player_inv_dist, enemyType, size,
                                 enemy_facing_direction, player_direction, health, state, cooldown])
        return np.asarray(self.enemies)

    def get_sprites(self, level):
        self.sword_sprites = []
        self.enemy_sprites = [[], []]
        select_weapon = np.random.randint(0, 2)
        enemy_sheet = pg.image.load('Assets/Sprites/zombie_n_skeleton' + str(level) + '.png').convert_alpha()
        if select_weapon == 0:
            sword_sheet = pg.image.load('Assets/Sprites/sword2.png').convert_alpha()
        elif select_weapon == 1:
            sword_sheet = pg.image.load('Assets/Sprites/gun2.png').convert_alpha()
        for column in range(3):
            self.sword_sprites.append(pg.Surface.subsurface(sword_sheet, (column * 800, 0, 800, 600)))
            x_offset = column * 32
            self.enemy_sprites[0].append([])
            self.enemy_sprites[1].append([])

            for row in range(4):
                y_offset = row * 100
                self.enemy_sprites[0][column].append(pg.Surface.subsurface(enemy_sheet, (x_offset, y_offset, 32, 100)))
                self.enemy_sprites[1][column].append(
                    pg.Surface.subsurface(enemy_sheet, (x_offset + 96, y_offset, 32, 100)))
        enemy_sprite_size = np.asarray(self.enemy_sprites[0][1][0].get_size())
        self.sword_sprites.append(self.sword_sprites[1])
        current_sword_sprite = 0
        return self.enemy_sprites, enemy_sprite_size, self.sword_sprites, current_sword_sprite, select_weapon


@njit(cache=True)
def enemies_ai(pos_x, pos_y, enemies, map_height, size, enemies_heatmap, current_sword_sprite,
               ticks, health, number_enemies, level=0):
    if number_enemies < 5:  # телепорт врагов поближе
        for enemy_id in range(len(enemies)):
            if enemies[enemy_id][8] > 0:
                enemy_x, enemy_y = enemies[enemy_id][0], enemies[enemy_id][1]
                distance_to_player = np.sqrt((enemy_x - pos_x) ** 2 + (enemy_y - pos_y) ** 2 + 1e-16)
                if distance_to_player > 10:
                    for _ in range(10):
                        random_x, random_y = np.random.randint(1, size), np.random.randint(1, size)
                        distance_to_player = np.sqrt((random_x + 0.5 - pos_x) ** 2 +
                                                     (random_y + 0.5 - pos_y) ** 2 + 1e-16)
                        if 6 < distance_to_player < 8 and map_height[random_x][random_y] == 0:
                            enemies[enemy_id][0], enemies[enemy_id][1] = random_x + 0.5, random_y + 0.5
                            break

    for enemy_id in range(len(enemies)): # изменение тепловой карты те карты врагов
        if enemies[enemy_id][8] > 0:
            grid_x, grid_y = int(enemies[enemy_id][0]), int(enemies[enemy_id][1])
            enemies_heatmap[grid_x - 1:grid_x + 2, grid_y - 1:grid_y + 2] += 1

    for enemy_id in range(len(enemies)): # определение состония врага 1 0 - норм 1 - зло 2 - защита
        if enemies[enemy_id][8] > 0 and np.random.uniform(0, 1) < 0.1:
            enemy_x, enemy_y, enemy_angle = (enemies[enemy_id][0],
                                             enemies[enemy_id][1], enemies[enemy_id][6])
            enemy_health, enemy_state, last_attack = (enemies[enemy_id][8],
                                                      enemies[enemy_id][9], enemies[enemy_id][10])
            distance_to_player = np.sqrt((enemy_x - pos_x) ** 2 + (enemy_y - pos_y) ** 2 + 1e-16)

            nearby_enemies = enemies_heatmap[int(enemy_x)][int(enemy_y)] - 1
            if distance_to_player > 1.42:
                nearby_enemies += enemies_heatmap[int(pos_x)][int(pos_y)]

            is_brave = 0
            if (enemy_health > 1 + enemies[enemy_id][4] - level or
                    enemy_health + nearby_enemies > 3 + enemies[enemy_id][4] - level):
                is_brave = 1

            if enemy_state == 0 and distance_to_player < 6:
                enemy_angle = calculate_angle(enemy_x, enemy_y, pos_x, pos_y)
                angle_difference = (enemies[enemy_id][6] - enemy_angle) % (2 * np.pi)
                if (angle_difference > 11 * np.pi / 6 or angle_difference < np.pi / 6
                        or (current_sword_sprite >= 1 and distance_to_player < 3)):
                    if check_visibility(pos_x, pos_y, enemy_x, enemy_y, distance_to_player, map_height, size):
                        if is_brave and ticks - last_attack > 5:
                            enemy_state = 1
                        elif distance_to_player < 2:
                            enemy_state = 2
                            enemy_angle -= np.pi
                    else:
                        enemy_angle = enemies[enemy_id][6]

            elif enemy_state == 1:
                if distance_to_player < 0.8 and ticks - last_attack > 10:
                    enemies[enemy_id][10] = ticks
                    health -= (np.random.uniform(0.1, 1 + level / 3) /
                               np.sqrt(1 + enemies_heatmap[int(pos_x)][int(pos_y)]))
                    enemy_state = 2
                if is_brave:
                    enemy_angle = calculate_angle(enemy_x, enemy_y, pos_x, pos_y)
                else:
                    enemy_state = 2

            elif enemy_state == 2:
                if is_brave and ticks - last_attack > 5:
                    enemy_state = 0
                else:
                    enemy_angle = (calculate_angle(pos_x, pos_y, enemy_x, enemy_y) +
                                   np.random.uniform(-0.5, 0.5))

            enemies[enemy_id][6], enemies[enemy_id][9] = (enemy_angle +
                                                                    np.random.uniform(-0.2, 0.2), enemy_state)

    return enemies, health, enemies_heatmap


@njit(cache=True)
def sort_sprites(pos_x, pos_y, rot, enemies, map_height, size, enemy_reaction, select_weapon):
    for enemy_index in range(len(enemies)):
        enemies[enemy_index][3] = 9999
        if enemies[enemy_index][8] > 0:  # Пропускаем мертвых врагов
            enemy_x, enemy_y = enemies[enemy_index][0], enemies[enemy_index][1]
            movement_direction = 1
            if enemies[enemy_index][9] == 1 and 1.7 < enemies[enemy_index][3] < 10:
                movement_direction = -1  # Избегаем приближения к игроку
            movement_speed = movement_direction * enemy_reaction * (1 + select_weapon + enemies[enemy_index][9] / 2)
            cos_angle, sin_angle = (movement_speed * np.cos(enemies[enemy_index][6]),
                                    movement_speed * np.sin(enemies[enemy_index][6]))
            new_x, new_y = enemy_x + cos_angle, enemy_y + sin_angle
            enemy_x, enemy_y = check_walls(enemy_x, enemy_y, map_height, new_x, new_y)
            if enemy_x == enemies[enemy_index][0] and enemy_y == enemies[enemy_index][1]:
                new_x, new_y = enemy_x - cos_angle, enemy_y - sin_angle
                enemy_x, enemy_y = check_walls(enemy_x, enemy_y, map_height, new_x, new_y)
                if enemy_x == enemies[enemy_index][0] and enemy_y == enemies[enemy_index][1]:
                    if map_height[int(new_x)][int(new_y)] == 0:
                        enemy_x, enemy_y = new_x, new_y
            if enemy_x == enemies[enemy_index][0] or enemy_y == enemies[enemy_index][1]:  # Проверяем столкновения
                enemies[enemy_index][6] = enemies[enemy_index][6] + np.random.uniform(-0.5, 0.5)
                if np.random.uniform(0, 1) < 0.01:
                    enemies[enemy_index][9] = 0  # Возвращаемся в нормальное состояние
            enemies[enemy_index][0], enemies[enemy_index][1] = enemy_x, enemy_y

            angle_to_player = calculate_angle(pos_x, pos_y, enemy_x, enemy_y)
            relative_angle = (rot - angle_to_player) % (2 * np.pi)
            if relative_angle > 10.5 * np.pi / 6 or relative_angle < 1.5 * np.pi / 6:
                direction_to_player = ((enemies[enemy_index][6] - angle_to_player - 3 * np.pi / 4) %
                                       (2 * np.pi)) / (np.pi / 2)
                distance_to_player = np.sqrt((enemy_x - pos_x) ** 2 + (enemy_y - pos_y) ** 2 + 1e-16)
                enemies[enemy_index][2] = relative_angle
                enemies[enemy_index][7] = direction_to_player
                if check_visibility(enemy_x, enemy_y, pos_x, pos_y, distance_to_player, map_height, size):
                    enemies[enemy_index][3] = 1 / distance_to_player

    enemies = enemies[enemies[:, 3].argsort()]
    return enemies