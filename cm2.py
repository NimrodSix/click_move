#!/usr/bin/python3.9

import pygame
import sys
import random

__author__ = "NimrodSix"
__email__ = "NimrodTH6 at gmail dot com"
__version__ = "0.2"
# __all__ = ["Creature", "Zoo", "ancestor"] # import cm2.py returns these


# ====================================================
def draw_text(text, x, y):
    font = pygame.font.SysFont('TSCu_Comic', 20, 'BOLD')
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))


# ====================================================
# TODO: Version 3 won't store anything... just return the subimage, since thats what im doing anyway
class SpriteSheet2:
    'Generic Sprite sheet. Feed me filename, columns & rows.'
    def __init__(self, filename: str, columns: int, rows: int):
        print('SpriteSheet.__init__({}. {}. {})'.format(filename, columns, rows))
        tile_sheet = pygame.image.load(filename)
        self.image_library = {}
        self.columns = columns
        self.rows = rows
        width, height = tile_sheet.get_size()
        self.image_width = int(width / columns)
        self.image_height = int(height / rows)

        for cy in range(rows):
            for cx in range(columns):
                rectangle = pygame.Rect(cx * self.image_width, cy * self.image_height, self.image_width,
                                        self.image_height)  # x, y, w, h
                self.image_library[(cx, cy)] = tile_sheet.subsurface(rectangle)
                #print('({}, {}):{} - '.format(cx, cy, rectangle), end='')
        print()

    def get(self, x, y):
        """ Returns image[(x, y)] """
        return self.image_library[(x, y)]
    
    # TODO: Should return a rectangle
    def width(self):
        return self.image_width

    def height(self):
        return self.image_height
    
    def columns(self):
        return self.columns

    def rows(self):
        return self.rows

# ====================================================
class ClickableImage:
    """ Holds an image and dimensions. Draw, move, click. """
    def __init__(self, screen, img, x, y):
        self.screen = screen
        self.image = img
        width, height = self.image.get_size()
        self.rectangle = Rect(x, y, width, height)
        
    def draw(self):
        self.screen.blit(self.image, (self.rectangle.left, self.rectangle.top))
        
    def move(self, x, y):
        self.rectangle.left = x
        self.rectangle.top = y
        
    def contains(self, x, y):
        if self.rectangle.collidepoint(x, y):
            return True
        return False
    
# ====================================================
class ClickableImageManager:
    """  Had trouble locking. This works much better """
    
    ss = SpriteSheet2("bb_font.png", 10, 5)

    def __init__(self, screen):
        self.selected = -1
        self.CIMList = []
        
        w = ClickableImageManager.ss.width()
        h = ClickableImageManager.ss.height()
        self.w_half = int(w / 2)    # Cursor holds image in middle
        self.h_half = int(h / 2)
        for yc in range(ClickableImageManager.ss.rows):
            for xc in range(ClickableImageManager.ss.columns):
                self.CIMList.append(ClickableImage(screen, ClickableImageManager.ss.get(xc, yc).convert(), xc * w, yc * h))
        
    def update_all(self, event):
        if self.selected == -1:                                     # If none are selected
            if event.type == pygame.MOUSEBUTTONDOWN:                # And theres a click
                for count, ci in enumerate(self.CIMList):
                    if ci.contains(event.pos[0], event.pos[1]):     # On an image
                        if event.button == 1:                       # With button 1 == LMB
                            # TODO: Move ci to the front of the list. (Move it up in Z order)
                            self.selected = count                   # Select it
                            break
        else:                                                       # If we have a selection
            if event.type == pygame.MOUSEMOTION:                    # Move it
                self.CIMList[self.selected].move(event.pos[0] - self.w_half, event.pos[1] - self.h_half)
            if event.type == pygame.MOUSEBUTTONDOWN:                # Or a button down
                self.selected = -1                                  # Deselect
                
    def draw_all(self):
        for ci in self.CIMList:
            ci.draw()

    
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Click Move Test')
screen = pygame.display.set_mode((640, 480), 0, 32)

# Setup globals ---------------------------------------- #
ci_manager = ClickableImageManager(screen)

# Loop ------------------------------------------------------- #
while True:
    
    # Background --------------------------------------------- #
    screen.fill(0)

    # Screen ------------------------------------------------- #
    ci_manager.draw_all()
        
    # Events ------------------------------------------------- #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        ci_manager.update_all(event)
        
    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
