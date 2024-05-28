import pygame as pg
from data.classes.settings import *
class MovingBlock(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.updatingBlockGroup
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("data/images/movingBlock.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.image.set_colorkey((0,0,0))
        
        self.dx = 0
        self.dy = 0
        
        self.game = game

    def collideWithWalls(self):
        for wall in self.game.walls:
            
            if wall.x == self.x + self.dx and wall.y == self.y + self.dy:
                self.game.blockIsMoving = False
                return True

        return False
        
    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def collideWithTile(self, tile):
        if tile.x == self.x and tile.y == self.y:
            return True
        else:
            return False
        
    def setVelocity(self, dx, dy):
        self.game.movingBlockSound.play()
        self.dx = dx
        self.dy = dy
        
    def movetoCoordinate(self, x, y):
        self.x = x
        self.y = y
        
    def update(self):
        tempBoolean = self.collideWithWalls()

        if not tempBoolean and self.game.blockIsMoving:
            self.move(self.dx, self.dy)

        if self.game.currentLevel > TELEPORTLEVEL:
            if self.collideWithTile(self.game.secondTeleporter):
                if self.game.canTeleport:
                    self.game.movingBlock.movetoCoordinate(self.game.firstTeleporter.x, self.game.firstTeleporter.y)
                    self.game.teleportSound.play()        
            
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
