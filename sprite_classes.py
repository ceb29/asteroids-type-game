import pygame

from pygame.constants import RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super(Player, self).__init__()
        self.surf1 = pygame.image.load("player_sprite1.png").convert()
        self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (screen_width/2,screen_height/2))
        self.front = 1
        self.front_last = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = pygame.mouse.get_pos()
    
    def update_position(self, pressed_key):
        if pressed_key[K_RIGHT]:
            if self.rect.right < self.screen_height:
                self.rect.move_ip(10, 0)
        elif pressed_key[K_LEFT]:
            if self.rect.left > 0:
                self.rect.move_ip(-10, 0) 
        elif pressed_key[K_UP]:
           if self.rect.top > 5:
              self.rect.move_ip(0, -10) 
        elif pressed_key[K_DOWN]:
            if self.rect.bottom < (self.screen_height):
                self.rect.move_ip(0, 10)
