from asteroids import COLOR_WHITE
import pygame
import math
#need to account for negative angle
#just use sin(-x) = -sin(x), cos(-x) = cos (x)
#import direction_angles 
#need to make a parent class with rotate and out of bounds
from pygame.constants import RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

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
        self.move_speed_x = 0 
        self.move_speed_y = 0
        self.x = 0
        self.y = 0

    def get_center_position(self):
        return self.center_position
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_rotation_angle(self):
        return self.rotation_angle

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
    
    def out_of_bounds(self):
        if self.rect.right > self.screen_width:
            self.rect.move_ip(-self.screen_height, 0)
        if self.rect.left < 0:
            self.rect.move_ip(self.screen_height, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, self.screen_height)
        if self.rect.bottom > self.screen_height:
            self.rect.move_ip(0, -self.screen_height) 

    def check_keys(self, pressed_key):
        if pressed_key[K_RIGHT]:
            self.rotate("right")
        if pressed_key [K_LEFT]:
            self.rotate("left")
        if pressed_key [K_UP]:
            self.move_speed_x += 0.2*self.x
            self.move_speed_y += 0.2*self.y
            self.surf1 = pygame.image.load("player_sprite2.png").convert()
            self.surf1 = pygame.transform.rotate(self.surf1, self.rotation_angle)
            self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
        else:
            self.surf1 = pygame.image.load("player_sprite1.png").convert()
            self.surf1 = pygame.transform.rotate(self.surf1, self.rotation_angle)
            self.surf1.set_colorkey((0, 0, 0), RLEACCEL)

    def update_position(self, pressed_key):
        self.x = math.sin(self.rotation_angle*math.pi/180) #get sin value for x term based on rotation angle 
        self.y = math.cos(self.rotation_angle*math.pi/180) #get cos value for y term
        self.out_of_bounds()
        self.rect.move_ip(-self.move_speed_x,-self.move_speed_y)
        self.center_position = [self.rect.centerx, self.rect.centery] #update position after moving
        #x = direction_angles.sin_angle[self.rotation_angle] #need to account for negative angles
        #y = direction_angles.cos_angle[self.rotation_angle]
        self.check_keys(pressed_key)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, center_position, player_x, player_y, player_size, screen_width, screen_height, rotation_angle):
        super(Projectile, self).__init__()
        self.surf1 = pygame.Surface((2, 2))
        self.surf1.fill(COLOR_WHITE)
        self.player_size = player_size
        self.player_x = player_x #maybe create tuples to clean up a bit
        self.player_y = player_y
        self.x = center_position[0] - 30 * player_x #puts projectile at tip of player based on rotation
        self.y = center_position[1] - 30 * player_y
        self.rect = self.surf1.get_rect(center = (self.x, self.y)) 
        self.orientation_flag = 0
        self.p_speed = 15
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.travel_distance = 0
        self.move_speed_x = 0
        self.move_speed_y = 0
        self.rotation_angle = rotation_angle #if an image is added could rotate

    def out_of_bounds(self):
        if self.rect.right > self.screen_width:
            self.rect.move_ip(-self.screen_height, 0)
        if self.rect.left < 0:
            self.rect.move_ip(self.screen_height, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, self.screen_height)
        if self.rect.bottom > self.screen_height:
            self.rect.move_ip(0, -self.screen_height)

    def update(self):
        #change firing position based off player orientation
        #keep updating position until out of bounds
        self.out_of_bounds()
        if self.travel_distance < self.screen_width:
            self.move_speed_x = -10*self.player_x #negative value moves in positive x direction
            self.move_speed_y = -10*self.player_y
            self.rect.move_ip(self.move_speed_x, self.move_speed_y)
            self.travel_distance += self.p_speed
        else:
            self.kill()