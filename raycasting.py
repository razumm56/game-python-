import numpy as np
from numba import njit


@njit(cache=True)
def new_frame(pos_x, pos_y, rot, frame, sky, floor, hres, halfvres, mod, map_height, size, wall, map_color,
              exit_x, exit_y, rot_v, door, window, b_wall, exit_2):
    vertical_offset = -int(halfvres * rot_v)
    for i in range(hres):
        current_rot = rot + np.deg2rad(i / mod - 30)
        sin_rot, cos_rot, cos_rot2 = np.sin(current_rot), np.cos(current_rot), np.cos(np.deg2rad(i / mod - 30))
        frame[i][:] = sky[int(np.rad2deg(current_rot) * 2 % 720)][halfvres - vertical_offset:3 * halfvres - vertical_offset] # отрисовка неба

        dist_to_lower_wall = 0
        dist_to_upper_wall = 0
        x, y = pos_x + 0.2 * cos_rot, pos_y + 0.2 * sin_rot
        for j in range(2000):
            x, y = x + 0.01 * cos_rot, y + 0.01 * sin_rot
            if dist_to_lower_wall == 0 and map_height[int(x) % (size - 1)][int(y) % (size - 1)] != 0:  # расстояние до нижней стены
                dist_to_lower_wall = np.sqrt((x - pos_x) ** 2 + (y - pos_y) ** 2)
            if map_height[int(x) % (size - 1)][int(y) % (size - 1)] == 2:  # расстояние до верхней
                dist_to_upper_wall = np.sqrt((x - pos_x) ** 2 + (y - pos_y) ** 2)
                height_upper_wall = halfvres / (dist_to_upper_wall * cos_rot2 + 0.001)
                break
        current_wall = wall

        if dist_to_upper_wall > 0.5 and 3 * height_upper_wall > int(halfvres / (dist_to_lower_wall * cos_rot2 + 0.000001)):  # отрисовка верхней стены
            xx = int(x * 3 % 1 * 99)
            xxx = x % 1
            if x % 1 < 0.01 or x % 1 > 0.99:
                xx = int(y * 3 % 1 * 99)
                xxx = y % 1
            yy = np.linspace(0, 3, int(height_upper_wall * 2)) * 99 % 99

            shade = 0.3 + 0.7 * (height_upper_wall / halfvres)
            if shade > 1:
                shade = 1

            if map_height[int(x - 0.02) % (size - 1)][int(y - 0.02) % (size - 1)] != 0:
                shade = shade * 0.8

            color = shade * map_color[int(x) % (size - 1)][int(y) % (size - 1)]
            if dist_to_upper_wall > 3.5:
                current_wall = b_wall
            for k in range(int(height_upper_wall) * 2):
                color2 = color * current_wall[xx][int(yy[k])]
                h1 = int(halfvres - int(height_upper_wall) + k + vertical_offset - 2 * height_upper_wall + 3)
                h2 = int(halfvres + 3 * height_upper_wall - k + vertical_offset - 1 + 2 * height_upper_wall - 6)
                if xxx > 1 / 3 and xxx < 2 / 3 and k > height_upper_wall * 2 / 3 and k < height_upper_wall * 4 / 3:
                    color2 = shade * window[xx][int(yy[k])]
                if h1 >= 0 and h1 < 2 * halfvres:
                    frame[i][h1] = color2
                if h2 < halfvres * 2:
                    frame[i][h2] = color2

        if dist_to_lower_wall == 0: #отрисовка нижней стены
            dist_to_lower_wall = 1000
        x, y = pos_x + dist_to_lower_wall * cos_rot, pos_y + dist_to_lower_wall * sin_rot
        wall_type = map_height[int(x) % (size - 1)][int(y) % (size - 1)]
        current_wall = wall
        if dist_to_lower_wall > 3.5:
            current_wall = b_wall
        height_lower_wall = int(halfvres / (dist_to_lower_wall * cos_rot2 + 0.000001))

        xx = int(x * 3 % 1 * 99)
        xxx = x % 1
        if x % 1 < 0.01 or x % 1 > 0.99:
            xx = int(y * 3 % 1 * 99)
            xxx = y % 1
        yy = np.linspace(0, 3, int(height_lower_wall * 2)) * 99 % 99

        shade = 0.4 + 0.6 * (height_lower_wall / halfvres)
        if shade > 1:
            shade = 1

        additional_shade = 0
        if map_height[int(x - 0.33) % (size - 1)][int(y - 0.33) % (size - 1)] != 0:
            additional_shade = 1

        if map_height[int(x - 0.01) % (size - 1)][int(y - 0.01) % (size - 1)] != 0:
            shade, additional_shade = shade * 0.7, 0

        color = map_color[int(x) % (size - 1)][int(y) % (size - 1)]
        door_color = np.sqrt(np.ones(3) - color)
        color = shade * color
        start_range, stop_range = 0, int(2 * height_lower_wall)
        if height_lower_wall > halfvres + abs(vertical_offset):
            start_range = int(height_lower_wall - halfvres - vertical_offset)
            stop_range = int(height_lower_wall + halfvres - vertical_offset)
        for k in range(start_range, stop_range):
            color2 = color * current_wall[xx][int(yy[k])]
            h1 = int(halfvres - height_lower_wall + k + vertical_offset)
            h2 = int(halfvres + 3 * height_lower_wall - k + vertical_offset - 3)
            if xxx > 1 / 3 and xxx < 2 / 3 and k > height_lower_wall * 2 / 3:
                if wall_type < 3:
                    color2 = shade * door_color * door[xx][int(yy[k])]
                elif k < height_lower_wall * 4 / 3 and wall_type == 3:
                    color2 = shade * window[xx][int(yy[k])]
            if h1 >= 0 and h1 < 2 * halfvres:
                if additional_shade and 1 - k / (2 * height_lower_wall) < 1 - xx / 99:
                    color2, color, additional_shade = 0.7 * color2, 0.7 * color, 0
                frame[i][h1] = color2
            if h2 < halfvres * 2:
                frame[i][h2] = color2


        for j in range(int(halfvres - height_lower_wall - vertical_offset)):  # отрисовка пола
            dist_to_floor = (halfvres / (halfvres - j - vertical_offset)) / cos_rot2
            x, y = pos_x + cos_rot * dist_to_floor, pos_y + sin_rot * dist_to_floor
            xx, yy = int(x * 3 % 1 * 99), int(y * 3 % 1 * 99)

            shade = min(0.2 + 0.8 / dist_to_floor, 1)
            if map_height[int(x - 0.33) % (size - 1)][int(y - 0.33) % (size - 1)] != 0:
                shade = shade * 0.7
            elif ((map_height[int(x - 0.33) % (size - 1)][int(y) % (size - 1)] and y % 1 > x % 1) or
                  (map_height[int(x) % (size - 1)][int(y - 0.33) % (size - 1)] and x % 1 > y % 1)):
                shade = shade * 0.7

            frame[i][halfvres * 2 - j - 1] = shade * (floor[xx][yy] * 2 + frame[i][halfvres * 2 - j - 1]) / 3

            if exit_2 == 0 and int(x) == exit_x and int(y) == exit_y and (x % 1 - 0.5) ** 2 + (y % 1 - 0.5) ** 2 < 0.2: # отрисовка колонны для выхода
                ee = j / (20 * halfvres)
                frame[i][j:2 * halfvres - j] = (ee * np.ones(3) * 255 + frame[i][j:2 * halfvres - j]) / (1 + ee)

    return frame


@njit(cache=True)
def check_visibility(pos_x, player_y, enemy_x, enemy_y, distance_to_player, map_height, map_size): #
    direction_cos, direction_sin = (pos_x - enemy_x) / distance_to_player, (player_y - enemy_y) / distance_to_player
    check_x, check_y = enemy_x, enemy_y
    is_visible = True
    check_x += 0.25 * direction_cos
    check_y += 0.25 * direction_sin

    for _ in range(abs(int((distance_to_player - 0.5) / 0.05))):
        check_x += 0.05 * direction_cos
        check_y += 0.05 * direction_sin
        # проверка видимости через map_height
        if (map_height[int(check_x - 0.02) % (map_size - 1)][int(check_y - 0.02) % (map_size - 1)] or
                map_height[int(check_x - 0.02) % (map_size - 1)][int(check_y + 0.02) % (map_size - 1)] or
                map_height[int(check_x + 0.02) % (map_size - 1)][int(check_y - 0.02) % (map_size - 1)] or
                map_height[int(check_x + 0.02) % (map_size - 1)][int(check_y + 0.02) % (map_size - 1)]):
            is_visible = False
            break

    return is_visible


@njit(cache=True)
def calculate_angle(pos_x, pos_y, enx, eny):
    angle = np.arctan((eny - pos_y) / (enx - pos_x + 1e-16))
    if abs(pos_x + np.cos(angle) - enx) > abs(pos_x - enx):
        angle = (angle - np.pi) % (2 * np.pi)
    return angle


@njit(cache=True)
def check_walls(pos_x, pos_y, map_height, x, y):
    if not (map_height[int(x - 0.2)][int(y)] or map_height[int(x + 0.2)][int(y)] or  # проверка всех сторон
            map_height[int(x)][int(y - 0.2)] or map_height[int(x)][int(y + 0.2)]):
        pos_x, pos_y = x, y

    elif not (map_height[int(pos_x - 0.2)][int(y)] or map_height[int(pos_x + 0.2)][int(y)] or  # движение по y
              map_height[int(pos_x)][int(y - 0.2)] or map_height[int(pos_x)][int(y + 0.2)]):
        pos_y = y

    elif not (map_height[int(x - 0.2)][int(pos_y)] or map_height[int(x + 0.2)][int(pos_y)] or  # движение по x
              map_height[int(x)][int(pos_y - 0.2)] or map_height[int(x)][int(pos_y + 0.2)]):
        pos_x = x

    return pos_x, pos_y

