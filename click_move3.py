#!/usr/bin/python3.9

import pygame
from pygame.locals import *
import sys
import random

__author__ = "NimrodSix"
__email__ = "NimrodTH6 at gmail dot com"
__version__ = "0.2"
__all__ = ["SpriteSheet", "ClickableImage", "ClickableImageManager"] # import cm2.py returns these


# ====================================================
def draw_text(text, x, y):
    font = pygame.font.SysFont('TSCu_Comic', 20, 'BOLD')
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))


# ====================================================
class SpriteSheet:
    """ Stores an image and returns sliced tiles on an x, y grid
    """
    def __init__(self, filename: str, columns: int, rows: int):
        self.tile_sheet = pygame.image.load(filename)
        width, height = self.tile_sheet.get_size()
        self.tile_width = int(width / columns)
        self.tile_height = int(height / rows)
        self.columns = columns
        self.rows = rows
        self.rectangle = pygame.Rect(0, 0, self.tile_width, self.tile_height) # x, y, w, h

    def get_image(self, x: int, y: int):
        self.rectangle.left = x * self.tile_width
        self.rectangle.top = y * self.tile_height
        return self.tile_sheet.subsurface(self.rectangle)


# ====================================================
class ClickableImage:
    """ Holds an image and dimensions. Draw, move, check clicks.
    """
    def __init__(self, screen, img, x, y):
        self.screen = screen
        self.image = img
        width, height = self.image.get_size()
        self.rectangle = Rect(x, y, width, height)
        self.x_offset = 0 # Storing click position relative to image rect
        self.y_offset = 0

    def draw(self):
        self.screen.blit(self.image, (self.rectangle.left, self.rectangle.top))
        
    def move(self, x, y):
        ' Change image location constraining it to the window '
        self.rectangle.left = x
        if self.rectangle.left < 0: # optimization needed
            self.rectangle.left = 0
        if self.rectangle.left > (int(self.screen.get_width()) - self.rectangle.width):
            self.rectangle.left = int(self.screen.get_width()) - self.rectangle.width

        self.rectangle.top = y
        if self.rectangle.top < 0:
            self.rectangle.top = 0
        if self.rectangle.top > (int(self.screen.get_height()) - self.rectangle.height):
            self.rectangle.top = int(self.screen.get_height()) - self.rectangle.height

    def contains(self, x, y):
        if self.rectangle.collidepoint(x, y):
            self.x_offset = x - self.rectangle.left # Where the image was clicked
            self.y_offset = y - self.rectangle.top
            return True
        return False


# ====================================================
class ClickableImageManager:
    """  Had trouble locking images to cursor. This works much better.
    """
    
    # Should hand it ss through init args
    ss = SpriteSheet("tokens.png", 14, 1)

    def __init__(self, screen):
        self.selected = -1  # Which image did we click?
        self.CIMList = []   # Storing a list of clickable images
        
        self.w = ClickableImageManager.ss.tile_width
        self.h = ClickableImageManager.ss.tile_height

        for yc in range(ClickableImageManager.ss.rows):
            for xc in range(ClickableImageManager.ss.columns):
                image = ClickableImageManager.ss.get_image(xc, yc)
                image.convert()
                image.convert_alpha()
                self.CIMList.append(ClickableImage(screen, image, xc * self.w, yc * self.h))
        
    def update_all(self, event):
        if self.selected == -1:                                                 # If none are selected
            if event.type == pygame.MOUSEBUTTONDOWN:                            # And theres a click
                for count, ci in enumerate(self.CIMList):
                    if ci.contains(event.pos[0], event.pos[1]):                 # On an image
                        if event.button == 1:                                   # With button 1 == LMB
                            self.CIMList.append(self.CIMList.pop(count))        # Move it to end of list
                            self.selected = len(self.CIMList) - 1               # Select it
                            break
        else:                                                                   # If we have a selection
            if event.type == pygame.MOUSEMOTION:                                # Move it using stored offset... smooth as butter!
                self.CIMList[self.selected].move(event.pos[0] - self.CIMList[self.selected].x_offset, event.pos[1] - self.CIMList[self.selected].y_offset)
            if event.type == pygame.MOUSEBUTTONDOWN:                            # Or a button down
                self.selected = -1                                              # Deselect
                
    def draw_all(self):
        for ci in self.CIMList:
            ci.draw()

    
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Click Move Test')
resolution_list = pygame.display.get_desktop_sizes()
print('Available resolutions: {}'.format(str(resolution_list)))
width, height = resolution_list[0]                              # Break out height to modify
screen = pygame.display.set_mode((width, height-100), 0, 32)    # Bottom of window was hiding behind KDE task bar

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
