#Asteroid type game made in python using pygame
import pygame
import random
import sprite_classes
#buttons used in game
from pygame.constants import K_RETURN, RLEACCEL, K_ESCAPE, KEYDOWN 
#create window and initialize
pygame.init()
player_size = 50
width, height = 750, 750
color_black = (0, 0, 0)
color_white = (255, 255, 255)
win = pygame.display.set_mode((width, height)) #creates a game window with given size 
font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text

class Update_Game():
    def __init__(self, surfaces, clock_speed, rgb_tuple):
        self.clock = pygame.time.Clock()
        self.surfaces = surfaces
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
    def draw_surfaces(self):
        for s in self.surfaces:
            win.blit(s.surf1, s.rect)
    #def update_sprite_pos():
    def update(self):
        win.fill(self.win_rgb)
        self.draw_surfaces()
        pygame.display.flip()
        self.clock.tick(60) 

def main():
    running = True
    clock = pygame.time.Clock()
    s1 = sprite_classes.Player(width, height)
    all_s = pygame.sprite.Group()
    all_s.add(s1)
    Game = Update_Game(all_s, 60, color_white)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
            elif event.type == pygame.QUIT:
                running = False
        Game.update()
        pressed_key = pygame.key.get_pressed()
        s1.update_position(pressed_key)
    pygame.quit()

if __name__ == "__main__":
    main()