import pygame as pg
from data.classes.settings import *
class ScoreKeeperBottom(pg.sprite.Sprite):

    
    def __init__(self, game):

        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)

        pg.sprite.Sprite.__init__(self)

        self.font = pg.font.Font('data/font/arcade.ttf', 16)

        self.score = 0

        self.previousScore = 0;

        self.message = "POINTS %-4d" % self.score
        self.image = self.font.render(self.message, 1, (0, 0, 0))        

        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT - 12
        self.rect.centerx = WIDTH - TILESIZE * 3
            
    def update(self):

        self.message = "POINTS %-4d" % self.score
        self.image = self.font.render(self.message, 1, (0, 0, 0))