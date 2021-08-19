import pygame
import sprite_classes

PLAYER_SIZE = 25
color_black= (0, 0, 0) #add file for colors
color_white = (255, 255, 255)
width, height = 1820, 980 #need to create file for constants

class Game_Text():
    def _init_(self, win):
        self.text_list = []
        self.font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text
        self.win = win
        self.game_status = 0
        self.score = 0
        self.high_score = 0
        self.game_over_width = (width/2) - 100
        self.game_over_height = (height/2) - 32
        self.score_padding = 125 
        self.high_score_padding = 200
        self.score_pad_num = 10
        self.high_score_pad_num = 10

    def get_status(self):
        return self.game_status

    def padding(self):
        if self.score / self.score_pad_num == 1:
            self.score_padding += 10
            self.score_pad_num *= 10

        if self.high_score / self.high_score_pad_num == 1:
            self.high_score_padding += 10
            self.high_score_pad_num *= 10

    def update_score(self):
        self.padding()
        if self.score > self.high_score:
            self.high_score = self.score
        self.text_list[3] = self.font.render(str(self.score), False, color_white)
        self.text_list[4] = self.font.render(str(self.high_score), False, color_white)
        
    def create_text(self):
        text_score = self.font.render('Score:', False, color_white)
        text_game_over = self.font.render('Game Over', False, color_white)
        text_high_score = self.font.render('High Score:', False, color_white)
        score = self.font.render(str(self.score), False, color_white)
        high_score = self.font.render(str(self.high_score), False, color_white)
        self.text_list = [text_score, text_game_over, text_high_score, score, high_score]  

    def update_text(self):
        if self.game_status == 0:
            self.update_score()
            self.win.blit(self.text_list[0], (5, 10)) #text_score
            self.win.blit(self.text_list[2], (0, height - 40))  #text_high_score
            self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
            self.win.blit(self.text_list[4], (self.high_score_padding, height - 40))  #high_score
        else:
            self.win.blit(self.text_list[0], (5, 10)) #text_score
            self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
            self.win.blit(self.text_list[1], (self.game_over_width, self.game_over_height)) #text_game_over
            self.win.blit(self.text_list[2], (5, height - 40)) #text_high_score
            self.win.blit(self.text_list[4], (self.high_score_padding, height - 40))  #high_score

class Game(Game_Text):
    def __init__(self, clock_speed, rgb_tuple, win):
        Game_Text._init_(self, win)
        self.player1 = sprite_classes.Player(width, height)
        self.projects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.num_enemies = 5
    
    def restart(self, status):
        if self.game_status == 1:
            self.player1 = sprite_classes.Player(width, height)
            self.start()
            self.game_status = status

    def start(self):
        self.create_text()
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
        self.update_text()
        pygame.display.flip()
        self.clock.tick(60) 

    def create_projectile(self):
        p1 = sprite_classes.Projectile(self.player1.get_center_position(), self.player1.get_x(), self.player1.get_y(), PLAYER_SIZE, width, height, self.player1.get_rotation_angle())
        self.surfaces.add(p1)
        self.projects.add(p1)

    def add_enemies(self, creation_flag, creation_type, center):
        for i in range(self.num_enemies):
            en = sprite_classes.Enemy(width, height, creation_flag, creation_type, center)
            self.enemies.add(en)
            self.surfaces.add(en)
    
    def add_sprites(self):
        self.surfaces.add(self.player1)
        self.add_enemies(0, 0, [0,0])

    def enemy_multiply(self, creation_type, center):
        if creation_type > 2:
            self.num_enemies = 2 #could make random, a certain number for each size, or certain amount of size 
            self.add_enemies(1, creation_type, center)

    def en_pro_collisions(self):
        #check for projectile and enemy collision
        for en in self.enemies:
            x = pygame.sprite.spritecollideany(en, self.projects)
            if x != None:
                x.kill()
                en.kill()
                self.enemy_multiply(en.get_creation_type(), en.get_center())
                self.score += 1
                #return 1
        #return 0

    def en_plr_collisions(self):
        #check for player collisions
        for en in self.enemies:
            if pygame.sprite.spritecollideany(self.player1, self.enemies, collided=pygame.sprite.collide_mask):
                self.game_status = 1
                self.score = 0
                return 1
        return 0

    def remove_sprites(self):
    #clean up sprites on game over
        self.player1.kill()
        for en in self.enemies:
            en.kill()
        for proj in self.projects:
            proj.kill()
        self.surfaces = pygame.sprite.Group()



           