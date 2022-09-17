from turtle import pos
import pygame as pg

class Character:
    def __init__(self, urlImg, pos, rot):
        self.image = pg.image.load(urlImg)
        self.position = pos
        self.rotation = rot

    def update(self, **flags):
        if any('pos' == key for key, val in flags.items()):
            self.position = pos
        