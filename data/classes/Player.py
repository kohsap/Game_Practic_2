import pygame as pg
from data.classes.settings import *
from data.classes.Immovable import Water
from data.classes.Movable import Free
class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        

        self.game = game
        
        self.currentFrame = 16
        self.image = self.game.playerSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        
        
    def movetoCoordinate(self, x, y):

        self.x = x
        self.y = y
         
    def setFrame(self, frameNumber):

        self.currentFrame = frameNumber
        
    def getFrame(self):

        return self.currentFrame
    
    def move(self, dx=0, dy=0):

        self.x += dx
        self.y += dy
                        

        self.game.moveSound.play()
        

        self.game.moved = True
            
    def checkAndMove(self, dx=0, dy=0):
        if self.game.currentLevel > MOVINGBLOCKLEVEL and self.nearTile(self.game.movingBlock) != 0:
            locationOfPlayer = self.nearTile(self.game.movingBlock)
            self.game.blockIsMoving = True
            
            if locationOfPlayer == 1 and dx == -1 and dy == 0:
                self.game.movingBlock.setVelocity(dx,dy)
            elif locationOfPlayer == 2 and dx == 1 and dy == 0:
                self.game.movingBlock.setVelocity(dx,dy)
            elif locationOfPlayer == 3 and dx == 0 and dy == -1:
                self.game.movingBlock.setVelocity(dx,dy)
            elif locationOfPlayer == 4 and dx == 0 and dy == 1:
                self.game.movingBlock.setVelocity(dx,dy)
            

            else:
                if not self.collideWithGroup(self.game.walls, dx, dy):
                    if self.checkMakeWater() and not self.collideWithGroup(self.game.noWaterGroup, 0, 0):
                        Water(self.game, self.x, self.y)
                    self.move(dx,dy)                    
        

        elif not self.collideWithGroup(self.game.walls, dx, dy):
            if self.checkMakeWater() and not self.collideWithGroup(self.game.noWaterGroup, 0, 0):
                Water(self.game, self.x, self.y)
            self.move(dx,dy)
                         
    def update(self):

        self.currentFrame += 1
        
        self.image = self.game.playerSpriteSheet.get_image(self.currentFrame)
        self.image.set_colorkey(BLUE)
        

        if self.currentFrame == 15:
            self.game.reset()
        
        if self.currentFrame == 86:
            self.currentFrame = 28 
        
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    
    
    def checkMakeWater(self):

        for ice in self.game.iceSprites:
            if ice.x == self.x and ice.y == self.y:
                ice.kill()
                Free(self.game, self.x, self.y)
                self.game.iceBreakSound.play()
                return False
            
        return True
    
        
    def collideWithGroup(self, nameOfGroup, dx=0, dy=0):
        ''' This method checks if the player has collison with a group's entities '''
 
        for entity in nameOfGroup:
            if entity.x == self.x + dx and entity.y == self.y + dy:
                return True
               
        return False
    
    def collideWithTile(self, tile):

        if tile.x == self.x and tile.y == self.y:
            return True
        else:
            return False

    def nearTile(self, tile):

        if tile.x == self.x - 1 and tile.y == self.y + 0:
            return 1
        elif tile.x == self.x + 1 and tile.y == self.y + 0:
            return 2
        elif tile.x == self.x + 0 and tile.y == self.y - 1:
            return 3
        elif tile.x == self.x + 0 and tile.y == self.y + 1:
            return 4
        
        return 0

        
    def checkDeath(self):

        left = False
        right = False
        top = False
        bottom = False

        for wall in self.game.walls:
            if wall.x == self.x - 1 and wall.y == self.y + 0:
                left = True
            elif wall.x == self.x + 1 and wall.y == self.y + 0:
                right = True
            elif wall.x == self.x + 0 and wall.y == self.y - 1:
                top = True
            elif wall.x == self.x + 0 and wall.y == self.y + 1:
                bottom = True             
        
        if left and right and top and bottom:
            Water(self.game, self.x, self.y)
            return True
        else:
            return False
            
