import pygame as pg

class Button(pg.sprite.Sprite):


    def __init__(self, game, buttonType, xCoordinate, yCoordinate, width, height):

        self.game = game

        self.groups = game.scoreSprites
        pg.sprite.Sprite.__init__(self, self.groups)

        if buttonType == "reset":
            self.buttonImages = ["data/images/resetButtonOne.png", "data/images/resetButtonTwo.png"]

        elif buttonType == "start":
            self.buttonImages = ["data/images/startButtonOne.png", "data/images/startButtonTwo.png"]

        elif buttonType == "play":
            self.buttonImages = ["data/images/playButtonOne.png", "data/images/playButtonTwo.png"]
        else:
            self.buttonImages = ["data/images/finishButtonOne.png", "data/images/finishButtonTwo.png"]

        self.width = width
        self.height = height

        self.buttonType = buttonType


        self.image = pg.image.load(self.buttonImages[0])
        

        self.image = pg.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.centery = yCoordinate
        self.rect.centerx = xCoordinate
        self.image.set_colorkey((255,255,255))
        
    def getRect(self):

        return self.rect
    
    def setImage(self, number):


        self.image = pg.image.load(self.buttonImages[number])

        self.image = pg.transform.scale(self.image, (self.width, self.height))
        
    def update(self):

        if self.getRect().collidepoint(pg.mouse.get_pos()):
            self.setImage(1)
        else:
            self.setImage(0)
