import numpy as np
import pygame as pg


class Map:

    @staticmethod
    def generate_map(size):
        map_color = np.random.uniform(0, 1, (size, size, 3))
        map_height = np.random.choice([0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4], (size, size))
        # установка границ карты
        map_height[0, :] = np.random.choice([1, 2, 3, 4], size)
        map_height[size - 1, :] = np.random.choice([1, 2, 3, 4], size)
        map_height[:, 0] = np.random.choice([1, 2, 3, 4], size)
        map_height[:, size - 1] = np.random.choice([1, 2, 3, 4], size)
        # инициализация начальной позиции и направления
        pos_x, pos_y = np.random.randint(1, size - 2) + 0.5, np.random.randint(1, size - 2) + 0.5
        rot, rot_v, step_count = np.pi / 4, 0, pos_x + pos_y
        current_x, current_y = int(pos_x), int(pos_y)
        map_height[current_x][current_y] = 0
        path_count = 0
        # генерация пути
        while True:
            test_x, test_y = (current_x, current_y)
            test_x += np.random.choice([-1, 1]) if np.random.uniform() > 0.5 else 0
            test_y += np.random.choice([-1, 1]) if np.random.uniform() <= 0.5 else 0
            if 0 < test_x < size - 1 and 0 < test_y < size - 1:
                if map_height[test_x][test_y] == 0 or path_count > 5:
                    path_count = 0
                    current_x, current_y = (test_x, test_y)
                    map_height[current_x][current_y] = 0
                    distance_to_start = np.sqrt((current_x - pos_x) ** 2 + (current_y - pos_y) ** 2)
                    if (distance_to_start > size * .6 and np.random.uniform() > .999) or np.random.uniform() > .99999:
                        exit_x, exit_y = (current_x, current_y)
                        break
                else:
                    path_count += 1

        return pos_x, pos_y, rot, rot_v, map_height, map_color, exit_x, exit_y, step_count

    @staticmethod
    def load_map(level):
        map_color = pg.surfarray.array3d(pg.image.load(f'Assets/Levels/map{level}.png'))
        size = len(map_color)
        map_height = np.random.choice([1, 2, 3, 4], (size, size))
        colors = np.array([[0, 0, 0], [255, 255, 255], [127, 127, 127]])
        pos_x, exit_x = None, None
        colonel_x, colonel_y = None, None
        for i in range(size):
            for j in range(size):
                color = map_color[i][j]
                if (color == colors[0]).all():
                    map_height[i][j] = 0
                    if (color == colors[1]).all():
                        pos_x, pos_y = i + 0.5, j + 0.5
                    elif (color == colors[2]).all():
                        exit_x, exit_y = i, j

        # если стартовая точка не найдена
        while pos_x is None:
            x, y = np.random.randint(1, size), np.random.randint(1, size)
            if (map_color[x][y] == colors[0]).all():
                pos_x, pos_y = x + 0.5, y + 0.5

        # если конечная точка не найдена
        while exit_x is None:
            x, y = np.random.randint(1, size), np.random.randint(1, size)
            if (map_color[x][y] == colors[0]).all():
                exit_x, exit_y = x, y

        rot, rot_v, step_count = np.pi / 4, 0, pos_x + pos_y

        return (pos_x, pos_y, rot, rot_v, map_height, map_color / 255, exit_x,
                exit_y, step_count, size)


