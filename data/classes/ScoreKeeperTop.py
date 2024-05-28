import pygame as pg
from data.classes.settings import *
class ScoreKeeperTop(pg.sprite.Sprite):

    def __init__(self, game):

        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)

        pg.sprite.Sprite.__init__(self)

        self.font = pg.font.Font('data/font/arcade.ttf', 16)

        self.currentLevel = 0
        self.completeTiles = 0
        self.totalTiles = 0
        self.solvedLevels = 0
        self.playerMelted = 0

        self.message = ""
        self.image = self.font.render(self.message, 1, (0, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.centery = TILESIZE - 15
        
        self.message = " "

        self.game = game
                    
    def checkFinish(self):

        return (self.completeTiles == self.totalTiles)      
          
    def update(self):

        self.message = "%11s%3d%20d%s%-20d%s%3d" % ( "LEVEL", self.currentLevel, self.completeTiles,\
                                                                               "/", self.totalTiles, "SOLVED", self.solvedLevels)
        self.image = self.font.render(self.message, 1, (0, 0, 0))