__author__ = 'Admin'

import pygame
import isoboard
import button
import os
import ast
import Tkinter
import tkFileDialog

from pygame.locals import *

class MapCreator:

    def __init__(self, surface):
        self.surface = surface
        self.iso = isoboard.IsoBoard.createBaseBoard()
        self.is_main = True
        self.moving = False
        self.addColButton = button.Button(self.makeText("Add Column"), self.addCol, rect = pygame.Rect(0,0,100,50))
        self.addRowButton = button.Button(self.makeText("Add Row"), self.addRow, rect = pygame.Rect(105,0,100,50))
        self.selectedTile = None
        self.heightChanging = False
        self.images = []
        self.spritesRect = pygame.Rect(105, self.surface.get_rect().height - 100, self.surface.get_rect().width - 110, 100)
        self.imageRects = []
        self.spritePaths = []
        self.imageLabels = []
        self.changingSprite = False
        self.saveMapButton = button.Button(self.makeText("Save"), self.exportToJSON, rect = pygame.Rect(0, self.surface.get_rect().height - 50, 100, 50))
        self.loadMapButton = button.Button(self.makeText("Open"), self.openMapFile, rect = pygame.Rect(0, self.surface.get_rect().height - 100, 100, 50))
        self.main_loop()


    def makeText(self, text):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        return self.font.render(text, True, (0,0,0))

    def changeSprite(self):
        self.changingSprite = True
        self.spritePaths = []
        imagePath = "images/map/"
        fileNames = [f for f in os.listdir(imagePath)]
        self.images = []
        for name in fileNames:
            self.images.append(pygame.image.load(imagePath + name))
            self.spritePaths.append(imagePath+name)
            self.imageLabels.append(self.makeText(name.split(".png")[0]))
        self.makeSpritesBox()

    def exportToJSON(self):
        json = self.iso.generateJSON()
        root = Tkinter.Tk()
        root.withdraw()
        file_path = tkFileDialog.asksaveasfilename(defaultextension='.mp')
        if file_path:
            f = open(file_path, "a")
            for x in json:
                f.write("{" + x + "}\n")
            f.close()

    def openMapFile(self):
        root = Tkinter.Tk()
        root.withdraw()
        file_path = tkFileDialog.askopenfilename()
        if file_path and file_path.split(".")[1] == "mp":
            f = open(file_path)
            json = []
            for line in f:
                json.append(line)
            f.close()
            self.createFromJSON(json)

    def createFromJSON(self, json):
        jsons = []
        for line in json:
            jsons.append(ast.literal_eval(line))
        self.iso = isoboard.IsoBoard.createFromJSON(jsons)


    def makeSpritesBox(self):
        self.imageRects = []
        self.labelRects = []
        i = 0
        for x in self.images:
            self.imageRects.append(pygame.Rect(110 + (i * (x.get_rect().width + 50)), self.surface.get_rect().height - 90, x.get_rect().width + 10, x.get_rect().height))
            self.labelRects.append(pygame.Rect(110 + (i * (x.get_rect().width + 50)), self.surface.get_rect().height - 40, x.get_rect().width + 10, x.get_rect().height))
            i += 1



    def update(self):
        if self.selectedTile:
            self.changeSprite()

    def addRow(self):
        self.iso.addRow()

    def addCol(self):
        self.iso.addColumn()

    def event_loop(self):
        for event in pygame.event.get():

            if event.type == QUIT:
                self.is_main = False
                pygame.quit()

            if event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    tile = self.iso.collidepoint(event.pos)
                    if tile:
                        if self.selectedTile:
                            self.iso.selectedTile = None
                        self.selectedTile = tile
                        self.iso.selectTile(tile)
                        self.heightChanging = True
                        self.startMovingPoint = event.pos

                if event.button == 3:
                    self.moving = True
                    self.startMovingPoint = event.pos

            if event.type == MOUSEBUTTONUP:

                if event.button == 1:
                    if self.changingSprite:
                        for rect, i in zip(self.imageRects, range(len(self.imageRects))):
                            if rect.collidepoint(event.pos):
                                self.selectedTile.changeSprite(self.spritePaths[i])
                    self.heightChanging = False
                    if self.addColButton.collidepoint(event.pos):
                        self.addColButton.callBack()

                    elif self.addRowButton.collidepoint(event.pos):
                        self.addRowButton.callBack()

                    elif self.saveMapButton.collidepoint(event.pos):
                        self.saveMapButton.callBack()

                    elif self.loadMapButton.collidepoint(event.pos):
                        self.loadMapButton.callBack()
                if event.button == 3:
                    self.moving = False

            if event.type == MOUSEMOTION:

                if self.selectedTile and self.heightChanging:
                    if event.pos[1] + 10 < self.startMovingPoint[1]:
                        self.selectedTile.changeHeight(self.selectedTile.height+1)
                        self.startMovingPoint = event.pos

                    elif event.pos[1] - 10 > self.startMovingPoint[1] and self.selectedTile.height > 1:
                        self.selectedTile.changeHeight(self.selectedTile.height-1)
                        self.startMovingPoint = event.pos

                if self.moving:
                    self.iso.setNewCoords((event.pos[0] - self.startMovingPoint[0], event.pos[1] - self.startMovingPoint[1]))
                    self.startMovingPoint = event.pos

    def main_loop(self):
        while self.is_main:
            self.event_loop()
            if self.is_main:
                self.update()
                self.draw(self.surface)

    def draw(self, surface):
        surface.fill((90,90,90))
        self.iso.drawTiles(surface)
        self.addColButton.draw(surface)
        self.addRowButton.draw(surface)
        self.saveMapButton.draw(surface)
        self.loadMapButton.draw(surface)
        if self.changingSprite:
            pygame.draw.rect(surface, (50,50,50), self.spritesRect)
            for image, rect in zip(self.images, self.imageRects):
                surface.blit(image, rect)
            for label, rect in zip(self.imageLabels, self.labelRects):
                surface.blit(label, rect)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    s = pygame.display.set_mode((800,600))
    s.fill((90,90,90))
    m = MapCreator(s)
    m.main_loop()
