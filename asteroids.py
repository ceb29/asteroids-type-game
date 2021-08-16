#Asteroid type game made in python using pygame

import pygame
import random

from pygame.constants import K_RETURN, RLEACCEL, K_ESCAPE, KEYDOWN #buttons used in game

pygame.init()
player_size = 50
width, height = 750, 750
color_black = (0, 0, 0)
win = pygame.display.set_mode((width, height)) #creates a game window with given size 
font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
            elif event.type == pygame.QUIT:
                running = False
        win.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick(60) 
    pygame.quit()

if __name__ == "__main__":
    main()