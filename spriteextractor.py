import pygame
class SpriteExtractor:
    def __init__(self):
        pass
    def extractSprites(self, size, f, pos=(0,0)):
        #Initial Values
        len_sprt_x,len_sprt_y = size #sprite size
        sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

        sheet = pygame.image.load(f) #Load the sheet
        sheet_rect = sheet.get_rect()
        sprites = []
        for i in range(0,sheet_rect.height-len_sprt_y + 1,size[1]):#rows
            for i in range(0,sheet_rect.width-len_sprt_x + 1,size[0]):#columns
                sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
                sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
                sprites.append(sprite)
                sprt_rect_x += len_sprt_x

            sprt_rect_y += len_sprt_y
            sprt_rect_x = 0
        return sprites
