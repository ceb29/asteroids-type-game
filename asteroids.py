#Asteroid type game made in python using pygame
#need to fix multiple input actions
import pygame
import sprite_classes
#buttons used in game
from pygame.constants import K_RETURN, RLEACCEL, K_ESCAPE, KEYDOWN, K_SPACE
#create window and initialize
pygame.init()
PLAYER_SIZE = 50
width, height = 1000, 1000
color_black= (0, 0, 0) #add file for colors
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

def create_projectile(player, all_s, projects):
    p1 = sprite_classes.Projectile(player.get_center_position(), player.get_x(), player.get_y(), PLAYER_SIZE, width, height, player.get_rotation_angle())
    all_s.add(p1)
    projects.add(p1)

def add_sprites(enemies, all_s ,enemies_list, s1):
    all_s.add(s1)
    for en in enemies_list:
        en = sprite_classes.Enemy(width, height)
        enemies.add(en)
        all_s.add(en)

def make_enemie_list(num_enemies):
    list1 = []
    for i in range(num_enemies):
        en = sprite_classes.Enemy(width, height)
        list1.append(en)
    return list1

def en_pro_collisions(projects, enemies, all_s):
    #check for projectile and enemy collision
    for en in enemies:
        if pygame.sprite.spritecollideany(en, projects):
            en.kill()
            return 1
    #return 0

def en_plr_collisions(s1, enemies):
    #check for player collisions
    for en in enemies:
        if pygame.sprite.spritecollideany(s1, enemies, collided=pygame.sprite.collide_mask):
            en.kill()
            return 1
    #return 0

def main():
    running = True
    s1 = sprite_classes.Player(width, height)
    projects = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_s = pygame.sprite.Group()
    enemy_start_count = 5
    enemie_list = make_enemie_list(enemy_start_count)
    add_sprites(enemies, all_s, enemie_list, s1)
    Game = Update_Game(all_s, 30, color_black)
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
        en_plr_collisions(s1, enemies)
        en_pro_collisions(projects, enemies, all_s)
        pressed_key = pygame.key.get_pressed()
        s1.update_position(pressed_key)
        projects.update()
        enemies.update()
    pygame.quit()

if __name__ == "__main__":
    main()