from sound import Sound
import numpy as np
import pygame as pg
import json

sound = Sound()


class Menu:
    @staticmethod
    def display_times(surface):
        font = pg.font.SysFont("Courier New", 45)
        with open('best_times.json', 'r') as file:
            file_data = json.load(file)
            times = file_data.get("passage_times", [])

        y_offset = 100  # Start position for the text
        header = font.render("Best Times:", True, (255, 255, 255))
        surface.blit(header, (50, y_offset))
        y_offset += 50

        for entry in times:
            for date_time, time in entry.items():
                text = f"{date_time}: {time}s"
                rendered_text = font.render(text, True, (255, 255, 255))
                surface.blit(rendered_text, (50, y_offset))
                y_offset += 40

    def pause_menu(self, surface, menu, pause, options, click, running, m_vol, sfx_vol, sound, newgame,
                   font, msg, level, ticks, hres, story):
        adjust_res = 1
        p_mouse = pg.mouse.get_pos()
        if options == 0:  # main menu
            if p_mouse[0] < 600 and p_mouse[1] > 200 and p_mouse[1] < 265:  # continue
                pg.draw.rect(surface, (150, 250, 150), (0, 200, 600, 65))
                if click:
                    if newgame == 2:
                        newgame, story = 1, 1
                    else:
                        pause = 0
                    pg.mouse.set_pos(400, 300)
            elif p_mouse[0] < 600 and p_mouse[1] > 300 and p_mouse[1] < 365:  # new game
                pg.draw.rect(surface, (150, 150, 250), (0, 300, 600, 65))
                if click:
                    if newgame == 0:
                        newgame = 1
                    else:
                        newgame, story = 1, 0
            elif p_mouse[0] < 600 and p_mouse[1] > 400 and p_mouse[1] < 465:  # options
                pg.draw.rect(surface, (150, 150, 150), (0, 400, 600, 65))
                if click:
                    options = 1
            elif p_mouse[0] < 600 and p_mouse[1] > 500 and p_mouse[1] < 565:  # leave
                pg.draw.rect(surface, (250, 150, 150), (0, 500, 600, 65))
                if click:
                    if newgame == 0:
                        newgame = 2
                    else:
                        running = 0

            elif p_mouse[0] > 679 and p_mouse[1] > 509:  # i button
                pg.draw.circle(surface, (250, 150, 150), (736, 556), 42)
                if click:
                    options = 2

            if newgame == 0:
                surface.blit(menu[3], (0, 0))
            else:
                surface.blit(menu[0], (0, 0))
            if newgame == 0:
                surface.blit(font.render(msg, 1, (255, 255, 255)), (30, 100 + 5 * np.sin(ticks - 1)))
                surface.blit(font.render(msg, 1, (30, 255, 155)), (32, 100 + 5 * np.sin(ticks)))
                surface.blit(font.render(str(level), 1, (255, 255, 255)), (675, 275 + 5 * np.sin(ticks - 1)))
                surface.blit(font.render(str(level), 1, (255, 100, 50)), (677, 275 + 5 * np.sin(ticks)))

        elif options == 1:  # options menu
            if p_mouse[0] > 50 and p_mouse[0] < 130 and p_mouse[1] > 220 and p_mouse[1] < 290:  # -resol
                pg.draw.rect(surface, (150, 250, 150), (60, 220, 70, 70))
                if click:
                    adjust_res = 0.9
            elif p_mouse[0] > 650 and p_mouse[0] < 720 and p_mouse[1] > 220 and p_mouse[1] < 290:  # +resol
                pg.draw.rect(surface, (150, 250, 150), (650, 220, 70, 70))
                if click:
                    adjust_res = 1.1
            elif click and p_mouse[0] > 123 and p_mouse[0] < 646 and p_mouse[1] > 360 and p_mouse[1] < 424:  #+ volume
                sfx_vol = (p_mouse[0] - 123) / 523
                sound.set_volume(m_vol, sfx_vol)
            elif click and p_mouse[0] > 123 and p_mouse[0] < 646 and p_mouse[1] > 512 and p_mouse[1] < 566:  #volume
                m_vol = (p_mouse[0] - 123) / 523
                sound.set_volume(m_vol, sfx_vol)

            surface.blit(menu[options], (0, 0))
            pg.draw.polygon(surface, (50, 200, 50),
                            ((123, 414), (123 + 523 * sfx_vol, 414 - 54 * sfx_vol), (123 + 520 * sfx_vol, 418)))
            pg.draw.polygon(surface, (50, 200, 50),
                            ((123, 566), (123 + 523 * m_vol, 566 - 54 * m_vol), (123 + 520 * m_vol, 570)))
            surface.blit(font.render(str(hres) + " x " + str(int(hres * 0.75)), 1, (255, 255, 255)),
                         (200, 220 + 5 * np.sin(ticks - 1)))
            surface.blit(font.render(str(hres) + " x " + str(int(hres * 0.75)), 1, (255, 100, 50)),
                         (202, 220 + 5 * np.sin(ticks)))

        elif options == 2:  # info times
            surface.blit(menu[options], (0, 0))
            self.display_times(surface)

        if options > 0 and p_mouse[0] > 729 and p_mouse[1] < 60:  # x button
            pg.draw.circle(surface, (0, 255, 0), (768, 31), 30)
            if click:
                options = 0
            surface.blit(menu[options], (0, 0))

        # draw cursor
        pg.draw.polygon(surface, (200, 50, 50), ((p_mouse), (p_mouse[0] + 20, p_mouse[1] + 22),
                                                 (p_mouse[0], p_mouse[1] + 30)))

        return surface, pause, options, running, newgame, adjust_res, m_vol, sfx_vol, story

    @staticmethod
    def splash_screen(msg, splash, clock, font, screen):
        running = 1
        clickdelay = 0
        while running:
            clickdelay += 1
            clock.tick(60)
            surf = splash.copy()
            ticks = pg.time.get_ticks() / 200
            surf.blit(font.render(msg, 1, (0, 0, 0)), (50, 450 + 5 * np.sin(ticks - 1)))
            surf.blit(font.render(msg, 1, (255, 255, 255)), (52, 450 + 5 * np.sin(ticks)))

            p_mouse = pg.mouse.get_pos()
            pg.draw.polygon(surf, (200, 50, 50),
                            ((p_mouse), (p_mouse[0] + 20, p_mouse[1] + 22), (p_mouse[0], p_mouse[1] + 30)))

            screen.blit(surf, (0, 0))
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN and clickdelay > 50:
                    return
                elif event.type == pg.QUIT:
                    pg.quit()
            if clickdelay == 180:
                msg = "Press any key..."

    @staticmethod
    def adjust_resolution(hres=250):
        hres = max(min(hres, 800), 80)
        halfvres = int(hres * 0.375)
        mod = hres / 60  #
        frame = np.random.randint(0, 255, (hres, halfvres * 2, 3))

        return hres, halfvres, mod, frame
