from raycasting import *
import pygame as pg


class Draw:
    @staticmethod
    def draw_sprites(surf, sprites, enemies, sprite_size, hres, halfvres, ticks, sword, current_sword_sprite, rot_v):
        offset = int(rot_v * halfvres)
        cycle = int(ticks) % 3
        for enemies_index in range(len(enemies)):
            if enemies[enemies_index][3] > 10:
                break
            types, dir2p = int(enemies[enemies_index][4]), int(enemies[enemies_index][7])
            cos2 = np.cos(enemies[enemies_index][2])
            scale = min(enemies[enemies_index][3], 2) * sprite_size * enemies[enemies_index][5] / cos2 * hres / 800
            vert = halfvres + halfvres * min(enemies[enemies_index][3], 2) / cos2 - offset
            hor = hres / 2 - hres * np.sin(enemies[enemies_index][2])
            if enemies[enemies_index][3] > 0.333:
                sp_surf = pg.transform.scale(sprites[types][cycle][dir2p], scale)
            else:
                sp_surf = pg.transform.smoothscale(sprites[types][cycle][dir2p], scale)
            surf.blit(sp_surf, (hor, vert) - scale / 2)

        sword_pos = (np.sin(ticks) * 10 * hres / 800, (np.cos(ticks) * 10 + 15) * hres / 800)  # sword shake
        sp_surf = pg.transform.scale(sword[int(current_sword_sprite)], (hres, halfvres * 2))
        surf.blit(sp_surf, sword_pos)

        return surf, enemies_index - 1

    @staticmethod
    def draw_colonel(surface, colonel, pos_x, pos_y, exit_x, exit_y, hres, halfvres, rot, rot_v, map_height, size):
        angle = calculate_angle(pos_x, pos_y, exit_x, exit_y)
        angle2 = (rot - angle) % (2 * np.pi)
        if angle2 > 10.5 * np.pi / 6 or angle2 < 1.5 * np.pi / 6:
            dist2p = np.sqrt((exit_x - pos_x) ** 2 + (exit_y - pos_y) ** 2 + 1e-16)
            if check_visibility(exit_x, exit_y, pos_x, pos_y, dist2p, map_height, size):
                offset = int(rot_v * halfvres)
                cos2 = np.cos(angle2)
                sp_size = np.asarray(colonel.get_size())
                scale = min(1 / dist2p, 2) * sp_size * 6 / cos2 * hres / 800
                vert = halfvres + halfvres * min(1 / dist2p, 2) / cos2 - offset
                hor = hres / 2 - hres * np.sin(angle2)
                if dist2p < 3:
                    sp_surf = pg.transform.scale(colonel, scale)
                else:
                    sp_surf = pg.transform.smoothscale(colonel, scale)
                surface.blit(sp_surf, (hor,vert) - scale / 2)
        return surface





