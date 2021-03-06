#need to figure out a way to fix audio pop on throttle with fade
#Asteroid type game made in python using pygame
import pygame
from asteroids_class import Asteroids
from pygame.constants import K_RETURN, K_ESCAPE, KEYDOWN, K_SPACE #buttons used in game
from constants import *

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.get_fonts()
    sound_files = ["./sound_files/shoot.wav", "./sound_files/thrust.wav", "./sound_files/asteroid.wav", "./sound_files/game_over.wav"]
    running = True
    game = Asteroids(30, COLOR_BLACK, sound_files)
    game.start()
    
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    game.write_high_score()
                    running = False
                if event.key == K_SPACE and game.get_status() == 0:
                        game.add_projectile()
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