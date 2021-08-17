#Asteroid type game made in python using pygame
#need to fix multiple input actions
import pygame
import random
import sprite_classes
#buttons used in game
from pygame.constants import K_RETURN, RLEACCEL, K_ESCAPE, KEYDOWN, K_SPACE
#create window and initialize
pygame.init()
PLAYER_SIZE = 50
width, height = 750, 750
color_black= (0, 0, 0) #add file for colors
COLOR_WHITE = (255, 255, 255)
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

def create_projectile(player, all_s, projects):
    p1 = sprite_classes.Projectile(player.get_center_position(), player.get_x(), player.get_y(), PLAYER_SIZE, width, height, player.get_rotation_angle())
    all_s.add(p1)
    projects.add(p1)

def main():
    running = True
    s1 = sprite_classes.Player(width, height)
    projects = pygame.sprite.Group()
    all_s = pygame.sprite.Group()
    all_s.add(s1)
    Game = Update_Game(all_s, 60, color_black)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
                if event.key == K_SPACE:
                    create_projectile(s1, all_s, projects)
            elif event.type == pygame.QUIT:
                running = False
        Game.update()
        pressed_key = pygame.key.get_pressed()
        s1.update_position(pressed_key)
        projects.update()
    pygame.quit()

if __name__ == "__main__":
    main()