import pygame
import math
import random
import sprite_dict
from pygame.constants import RLEACCEL, K_UP, K_LEFT, K_RIGHT
from constants import COLOR_WHITE, COLOR_BLACK
#need to account for negative angle
#just use sin(-x) = -sin(x), cos(-x) = cos (x)
#import direction_angles 

class Sprites(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, center):
        super(Sprites, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = center

    def get_center(self):
        return self.center

    def out_of_bounds(self):
        if self.rect.right > self.screen_width:
            self.rect.move_ip(-self.screen_width, 0)
        if self.rect.left < 0:
            self.rect.move_ip(self.screen_width, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, self.screen_height)
        if self.rect.bottom > self.screen_height:
            self.rect.move_ip(0, -self.screen_height) 

class Player(Sprites):
    def __init__(self, screen_width, screen_height):
        Sprites.__init__(self, screen_width, screen_height, [screen_width/2,screen_height/2])
        self.surf1 = pygame.image.load(sprite_dict.player_sprites[1]).convert()
        self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (screen_width/2,screen_height/2))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_bott_pos = [self.rect.top, self.rect.bottom]
        self.rotation_angle = 0
        self.rotation_speed_right = 1
        self.rotation_speed_left = 1
        self.move_speed_x = 0 
        self.move_speed_y = 0
        self.x = 0
        self.y = 0
        self.thrust_val = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_move_speed_x(self):
        return self.move_speed_x

    def get_move_speed_y(self):
        return self.move_speed_y

    def get_rotation_angle(self):
        return self.rotation_angle

    def get_thrust_val(self):
        return self.thrust_val

    def set_thrust_val(self, thrust_val):
        self.thrust_val = thrust_val

    def rotate(self, direction):
        if direction == "right":
            rotation = -self.rotation_speed_right
        else:
            rotation = self.rotation_speed_left
        self.rotation_angle += rotation
        if self.rotation_angle >= 360 or self.rotation_angle <= -360:
            self.rotation_angle = 0
        self.surf1 = pygame.image.load(sprite_dict.player_sprites[1]).convert()
        self.surf1 = pygame.transform.rotate(self.surf1, self.rotation_angle)
        self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (self.center[0], self.center[1])) 

    def check_keys(self, pressed_key):
        if pressed_key[K_RIGHT]:
            if self.rotation_speed_right < 7:
                self.rotation_speed_right += 0.25
            self.rotate("right")
        else:
            self.rotation_speed_right = 1
        if pressed_key [K_LEFT]:
            if self.rotation_speed_left < 7:
                self.rotation_speed_left += 0.25
            self.rotate("left")
        else:
            self.rotation_speed_left = 1
        if pressed_key [K_UP]:
            self.move_speed_x += 0.2*self.x
            self.move_speed_y += 0.2*self.y
            self.surf1 = pygame.image.load(sprite_dict.player_sprites[2]).convert()
            self.surf1 = pygame.transform.rotate(self.surf1, self.rotation_angle)
            self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
            self.thrust_val = 1
        else:
            self.surf1 = pygame.image.load(sprite_dict.player_sprites[1]).convert()
            self.surf1 = pygame.transform.rotate(self.surf1, self.rotation_angle)
            self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
            self.thrust_val = 0

    def update(self, pressed_key):
        self.x = math.sin(self.rotation_angle*math.pi/180) #get sin value for x term based on rotation angle 
        self.y = math.cos(self.rotation_angle*math.pi/180) #get cos value for y term
        self.out_of_bounds()
        self.rect.move_ip(-self.move_speed_x,-self.move_speed_y)
        self.center = [self.rect.centerx, self.rect.centery] #update position after moving
        #x = direction_angles.sin_angle[self.rotation_angle] #need to account for negative angles
        #y = direction_angles.cos_angle[self.rotation_angle]
        self.check_keys(pressed_key)

class Projectile(Sprites):
    def __init__(self, center, player_x, player_y, player_move_speed_x, player_move_speed_y, player_size, screen_width, screen_height, rotation_angle):
        Sprites.__init__(self, screen_width, screen_height, center)
        self.surf1 = pygame.Surface((2, 2))
        self.surf1.fill(COLOR_WHITE)
        self.player_size = player_size
        self.center = center
        self.player_x = player_x #maybe create tuples to clean up a bit
        self.player_y = player_y
        self.player_move_speed_x = player_move_speed_x
        self.player_move_speed_y = player_move_speed_y
        self.x = center[0] - 30 * player_x #puts projectile at tip of player based on rotation
        self.y = center[1] - 30 * player_y
        self.rect = self.surf1.get_rect(center = (self.x, self.y)) 
        self.orientation_flag = 0
        self.p_speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.travel_distance = 0
        self.move_speed_x = 0
        self.move_speed_y = 0
        self.rotation_angle = rotation_angle #if an image is added could rotate

    def update(self):
        #change firing position based off player orientation
        #keep updating position until out of bounds
        self.out_of_bounds()
        if self.travel_distance < self.screen_width:
            self.move_speed_x = -(self.p_speed*self.player_x + self.player_move_speed_x) #negative value moves in positive x direction
            self.move_speed_y = -(self.p_speed*self.player_y + self.player_move_speed_y)
            self.rect.move_ip(self.move_speed_x, self.move_speed_y)
            self.travel_distance += self.p_speed
        else:
            self.kill()

class Enemy(Sprites):
    def __init__(self, screen_width, screen_height, creation_flag, creation_type, center):
        Sprites.__init__(self, screen_width, screen_height, center)
        self.flag1 = random.randint(0, 3) 
        self.random_speed = random.randint(1, 3)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = center
        self.asteroid_type = 0
        if creation_flag == 0:
            self.asteroid_type = random.randint(1, 8)
            self.surf1 = pygame.image.load(sprite_dict.asteroid_sprites[self.asteroid_type]).convert()
            self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
            random_place = random.randint(1, 4)  #random starting place on outskirts of play area
            if random_place == 1:
                self.rect = self.surf1.get_rect(center = (random.randint(0, self.screen_width), 0))
            elif random_place == 2:
                self.rect = self.surf1.get_rect(center = (0, random.randint(0, self.screen_height)))
            elif random_place == 3:
                self.rect = self.surf1.get_rect(center = (random.randint(0, self.screen_width), self.screen_height))
            elif random_place == 4:
                self.rect = self.surf1.get_rect(center = (self.screen_width, random.randint(0, self.screen_height)))
        else:
            if self.asteroid_type % 2 != 0:
                self.asteroid_type = creation_type - 1 #changed this, added -1
            else:
                self.asteroid_type = creation_type - 2
            self.surf1 = pygame.image.load(sprite_dict.asteroid_sprites[self.asteroid_type]).convert()
            self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
            self.rect = self.surf1.get_rect(center = (self.center))
    
    def get_creation_type(self):
        return self.asteroid_type

    def update(self): 
        #change position on wall bounces
        #commented portions could be added to increase speed on every wall bounce
        if self.flag1 == 0:
            self.rect.move_ip(self.random_speed , self.random_speed)
        elif self.flag1 == 1:
            self.rect.move_ip(self.random_speed , -self.random_speed)
        elif self.flag1 == 2:
            self.rect.move_ip(-self.random_speed , -self.random_speed)
        elif self.flag1 == 3:
            self.rect.move_ip(-self.random_speed , self.random_speed)
        self.out_of_bounds()
        self.center = [self.rect.centerx, self.rect.centery]