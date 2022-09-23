import sys
import pygame as pg
from sprites import *

screen_size = (800, 600)
aspect_ratio = screen_size[0]/screen_size[1]

def scrPos(x, y):
    return (x, screen_size[1] - y)

def unit(x, y):
    return(x * screen_size[0] / (12 * aspect_ratio), screen_size[1] + y / screen_size[1] * 12)    

def main():
    pg.init()

    pg.display.set_caption("Epicka Hra")

    screen = pg.display.set_mode(screen_size, pg.NOFRAME)

    clock = pg.time.Clock()

    #active sprite group
    activeGroup = pg.sprite.Group()

    chad = Sprite("chad.png", )
    direction = [0, 0]

    #movement registerers
    player = {
        "left": False,
        "right": False,
        "jumpHeight": -10,
        "movementSpeed": 0.5
    }

    #player statuses initialization
    verticalVelocity = 1
    gravity = 0.36
    grounded = False

    chad.add(activeGroup)

    staticGroupFront = pg.sprite.Group()

    map1 = [Block("boatFence.png", 100, 100, scrPos(0,0))]

    for i in range(0, len(map1)):
        map1[i].add(staticGroupFront)

    running = True
    while(running):
        #Player statuses:
        if(chad.get_position()[1] > scrPos(0, 125)[1]):
            grounded = True
            verticalVelocity = 0
        else:
            verticalVelocity += gravity
            verticalVelocity = min(verticalVelocity, 15)
            grounded = False
        
        for event in pg.event.get():
            if (event.type == pg.QUIT):
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    player["right"] = True
                if event.key == pg.K_a:
                    player["left"] = True
                if event.key == pg.K_SPACE:
                    if grounded:
                        verticalVelocity = player["jumpHeight"]

            if event.type == pg.KEYUP:
                if event.key == pg.K_d:
                    player["right"] = False
                if event.key == pg.K_a:
                    player["left"] = False

        screen.fill((83, 92, 104))

        deltaTime = clock.get_time()

        direction[0] = (1 * player["right"] - 1 * player["left"]) * player["movementSpeed"] * deltaTime

        direction[1] = verticalVelocity

        activeGroup.update(direction)
        activeGroup.draw(screen)

        staticGroupFront.draw(screen)

        clock.tick(60)
        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()