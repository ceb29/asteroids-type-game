#need to figure out a way to fix audio pop on throttle with fade
#Asteroid type game made in python using pygame
import pygame
import sprite_classes
from game_classes import Asteroids, width, height
#buttons used in game
from pygame.constants import K_RETURN, RLEACCEL, K_ESCAPE, KEYDOWN, K_SPACE
#create window and initialize
color_black= (0, 0, 0) #add file for colors
color_white = (255, 255, 255)

pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((width, height)) #creates a game window with given size 
#font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text

def main():
    running = True    
    game = Asteroids(30, color_black, win)
    game.start()
    
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    game.write_high_score()
                    running = False
                if event.key == K_SPACE and game.get_status() == 0:
                        game.create_projectile()
                        game.shoot_audio()
                if event.key == K_RETURN and game.get_status() == 1:
                        game.restart()
            elif event.type == pygame.QUIT:
                game.write_high_score()
                running = False
        game.update()
    pygame.quit()

if __name__ == "__main__":
    main()