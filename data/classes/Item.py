import pygame as pg
from data.classes.settings import *

class Item(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Treasure(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.image = pg.image.load("data/images/treasure.png")
        self.image.set_colorkey((255,255,255))
        
        
class GoldenKey(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        
        self.currentFrame = 1
        self.image = self.game.keySpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        

    def update(self):
        self.currentFrame += 1
        
        self.image = self.game.keySpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)

        if self.currentFrame == 32:
            self.currentFrame = 1