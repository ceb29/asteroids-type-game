import pygame
import sprite_classes

PLAYER_SIZE = 25
color_black= (0, 0, 0) #add file for colors
color_white = (255, 255, 255)
width, height = 1820, 980 #need to create file for constants

class Game():
    def __init__(self, clock_speed, rgb_tuple, win):
        self.win = win
        self.player1 = sprite_classes.Player(width, height)
        self.projects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.num_enemies = 5
        self.enemie_list = []
    
    def start(self):
        self.make_enemie_list()
        self.add_sprites()

    def draw_surfaces(self):
        for s in self.surfaces:
            self.win.blit(s.surf1, s.rect)
    
    def update_sprite_pos(self):
        if self.en_plr_collisions() == 1:
            self.remove_sprites()
        self.en_pro_collisions()
        pressed_key = pygame.key.get_pressed()
        self.player1.update_position(pressed_key)
        self.projects.update()
        self.enemies.update()

    def update(self):
        self.win.fill(self.win_rgb)
        self.draw_surfaces()
        self.update_sprite_pos()
        pygame.display.flip()
        self.clock.tick(60) 

    def create_projectile(self):
        p1 = sprite_classes.Projectile(self.player1.get_center_position(), self.player1.get_x(), self.player1.get_y(), PLAYER_SIZE, width, height, self.player1.get_rotation_angle())
        self.surfaces.add(p1)
        self.projects.add(p1)

    def add_enemies(self, creation_flag, creation_type, center):
        for en in self.enemie_list:
            en = sprite_classes.Enemy(width, height, creation_flag, creation_type, center)
            self.enemies.add(en)
            self.surfaces.add(en)
    
    def add_sprites(self):
        self.surfaces.add(self.player1)
        self.add_enemies(0, 0, [0,0])

    def make_enemie_list(self):
        self.enemie_list = []
        for i in range(self.num_enemies):
            en = sprite_classes.Enemy(width, height, 0, 0, [0, 0])
            self.enemie_list.append(en)

    def enemy_multiply(self, creation_type, center):
        if creation_type > 2:
            self.num_enemies = 4
            self.make_enemie_list()
            self.add_enemies(1, creation_type, center)

    def en_pro_collisions(self):
        #check for projectile and enemy collision
        for en in self.enemies:
            x = pygame.sprite.spritecollideany(en, self.projects)
            if x != None:
                x.kill()
                en.kill()
                self.enemy_multiply(en.get_creation_type(), en.get_center())
                #return 1
        #return 0

    def en_plr_collisions(self):
        #check for player collisions
        for en in self.enemies:
            if pygame.sprite.spritecollideany(self.player1, self.enemies, collided=pygame.sprite.collide_mask):
                return 1
        return 0

    def remove_sprites(self):
    #clean up sprites on game over
        self.player1.kill()
        for en in self.enemies:
            en.kill()
        for proj in self.projects:
            proj.kill()
