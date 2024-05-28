import pygame as pg
class BeginMenu(pg.sprite.Sprite):


    def __init__(self, game):
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.menuImages = ['data/images/titleScreen.png', 'data/images/instructionScreen.png']
        
        self.image = pg.image.load(self.menuImages[0])
        
        self.rect = self.image.get_rect()
        
        
    def instructions(self):
        self.image = pg.image.load(self.menuImages[1])
        self.rect = self.image.get_rect()