import pygame
import math
#need to account for negative angle
#just use sin(-x) = -sin(x), cos(-x) = cos (x)
#import direction_angles 

from pygame.constants import RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE
from pygame.transform import rotate

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super(Player, self).__init__()
        self.surf1 = pygame.image.load("player_sprite1.png").convert()
        self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (screen_width/2,screen_height/2))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_position = [screen_width/2,screen_height/2]
        self.top_bott_pos = [self.rect.top, self.rect.bottom]
        self.rotation_angle = 0
        self.rotation_speed = 5

    def rotate(self, direction):
        if direction == "right":
            rotation = -self.rotation_speed
        else:
            rotation = self.rotation_speed
        self.rotation_angle += rotation
        if self.rotation_angle > 360 or self.rotation_angle < -360:
            self.rotation_angle = 0
        self.surf1 = pygame.image.load("player_sprite1.png").convert()
        self.surf1 = pygame.transform.rotate(self.surf1, self.rotation_angle)
        self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (self.center_position[0], self.center_position[1])) 
        

    def update_position(self, pressed_key):
        x = math.sin(self.rotation_angle*math.pi/180)
        y = math.cos(self.rotation_angle*math.pi/180)
        #x = direction_angles.sin_angle[self.rotation_angle] #need to account for negative angles
        #y = direction_angles.cos_angle[self.rotation_angle]
        if pressed_key[K_RIGHT]:
            self.rotate("right")
        elif pressed_key[K_LEFT]:
            self.rotate("left")
            # if self.rect.left > 0:
            #     self.rect.move_ip(-10, 0)
            # else:
            #     self.rect.move_ip(self.screen_height, 0)
        elif pressed_key[K_UP]:
            self.rect.move_ip(-10*x, -10*y)
            # if self.rect.top > 0:
            #   self.rect.move_ip(0, -10) 
            # else:
            #     self.rect.move_ip(0, self.screen_height)
        elif pressed_key[K_DOWN]:
            self.rect.move_ip(1,1)
            # if self.rect.bottom < (self.screen_height):
            #     self.rect.move_ip(0, 10)
            # else:
            #     self.rect.move_ip(0, -self.screen_height)
        self.center_position = [self.rect.centerx, self.rect.centery] #update position after moving
