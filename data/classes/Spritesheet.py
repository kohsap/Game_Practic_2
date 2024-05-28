import pygame as pg
import xml.etree.ElementTree as ET
class Spritesheet:

    def __init__(self, filename, xmlName):

        self.spritesheet = pg.image.load(filename).convert()

        self.xml = ET.parse(xmlName)
        self.root = self.xml.getroot() 

        frame = ""

    def get_image(self, frameNumber):

        frame = self.root.find(".//*[@name='%s.png']"% frameNumber)

        image = pg.Surface((int(frame.attrib['w']), int(frame.attrib['h'])))

        image.blit(self.spritesheet, (0, 0), (int(frame.attrib['x']), int(frame.attrib['y']), int(frame.attrib['w']), int(frame.attrib['h'])))
        return image