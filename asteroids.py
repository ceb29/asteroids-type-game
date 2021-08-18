#Asteroid type game made in python using pygame
#need to fix multiple input actions
import pygame
import sprite_classes
from game_class import Game, width, height
#buttons used in game
from pygame.constants import K_RETURN, RLEACCEL, K_ESCAPE, KEYDOWN, K_SPACE
#create window and initialize
color_black= (0, 0, 0) #add file for colors
color_white = (255, 255, 255)

pygame.init()
win = pygame.display.set_mode((width, height)) #creates a game window with given size 
font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text

def main():
    running = True    
    game = Game(30, color_black, win)
    game.start()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
                if event.key == K_SPACE:
                    game.create_projectile()
            elif event.type == pygame.QUIT:
                running = False
        game.update()
    pygame.quit()

if __name__ == "__main__":
    main()