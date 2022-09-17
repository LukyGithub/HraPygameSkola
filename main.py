import sys
import pygame as pg
from character import *

def main():
    pg.init()

    pg.display.set_caption("Epicka Hra")

    screen = pg.display.set_mode((240,180), pg.RESIZABLE)

    hello = Character("chad.png", (0, 0), (0, 0))
    hello.update(pos=(1, 0))

    running = True
    while(running):
        for event in pg.event.get():
            if (event.type == pg.QUIT):
                running = False

        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()