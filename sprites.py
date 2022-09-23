import pygame as pg
import sys

class Sprite(pg.sprite.Sprite):
    def __init__(self, imgUrl, width, height):
        pg.sprite.Sprite.__init__(self)
        self.position = [0,0]
        self.image = pg.image.load(imgUrl)
        self.image = pg.transform.scale(self.image, (width, height))
  
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def get_position(self):
        return(self.position)

    def update(self, direction):
        self.position[0] += direction[0]
        self.position[1] += direction[1]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
            
class Block(pg.sprite.Sprite):
    def __init__(self, imgUrl, width, height, position):
        pg.sprite.Sprite.__init__(self)

        self.position = position
        self.image = pg.image.load(imgUrl)
        self.image = pg.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position
