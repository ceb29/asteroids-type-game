import pygame
import random
import sprite_classes

PLAYER_SIZE = 25
color_black= (0, 0, 0) #add file for colors
color_white = (255, 255, 255)
width, height = 1820, 980 #need to create file for constants


class Game_Sounds:
    def __init__(self):
        self.sound_list = []
        self.channel_list = []
        
    def add_channels(self, sound_file):
        self.sound_list.append(pygame.mixer.Sound(sound_file))
        self.channel_list.append(pygame.mixer.Channel(len(self.sound_list) - 1))

    def play_audio(self, sound_index):
        self.channel_list[sound_index].play(self.sound_list[sound_index])

    def play_audio_loop(self, sound_index):
        self.channel_list[sound_index].play(self.sound_list[sound_index], loops = -1)

    def pause_audio(self, sound_index):
        self.channel_list[sound_index].stop()

class Game_Text():
    def __init__(self, win):
        self.text_list = []
        self.font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text
        self.win = win
        self.score = 0
        self.high_score = 0
        self.game_over_width = (width/2) - 100
        self.game_over_height = (height/2) - 32
        self.score_padding = 125 
        self.high_score_padding = 200
        self.score_pad_num = 10
        self.high_score_pad_num = 10
    
    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def set_score(self, score):
        self.score = score

    def set_high_score(self, high_score):
        self.high_score = high_score

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

    def update_text(self, game_status):
        if game_status == 0:
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

class Game():
    def __init__(self, clock_speed, rgb_tuple, win):
        self.win = win
        self.text = Game_Text(win)
        self.game_status = 0
        self.sounds = Game_Sounds()
        #sound_files/asteroids_shoot_t.wav"
        self.sound_files = ["sound_files/shoot.wav", "sound_files/thrust.wav", "sound_files/asteroid.wav"] 
        self.player1 = sprite_classes.Player(width, height)
        self.projects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.thrust_flag = 0
        self.enemie_count = 5
    
    def get_status(self):
        return self.game_status

    def start(self):
        self.create_sounds()
        self.read_high_score()
        self.text.create_text()
        self.add_sprites()

    def next_level(self):
        self.surfaces = pygame.sprite.Group()
        self.add_sprites()

    def restart(self):
        self.player1 = sprite_classes.Player(width, height)
        self.enemie_count = 5
        self.add_sprites()
        self.game_status = 0

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

    def thrust_on_off(self):
        if self.player1.get_thrust_val() == 1 and self.thrust_flag == 0:
            self.thrust_audio()
            self.thrust_flag = 1
        elif self.player1.get_thrust_val() == 0 and self.thrust_flag == 1:
            self.thrust_audio_pause()
            self.thrust_flag = 0

    def update(self):
        self.win.fill(self.win_rgb)
        self.text.update_text(self.game_status)
        if self.game_status == 0:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.thrust_on_off()
        else:
            self.thrust_audio_pause()
            self.thrust_flag = 0
        pygame.display.flip()
        self.clock.tick(60) 

    def create_projectile(self):
        p1 = sprite_classes.Projectile(self.player1.get_center_position(), self.player1.get_x(), self.player1.get_y(), PLAYER_SIZE, width, height, self.player1.get_rotation_angle())
        self.surfaces.add(p1)
        self.projects.add(p1)

    def add_enemies(self, creation_flag, creation_type, center, num_enemies):
        for i in range(num_enemies):
            en = sprite_classes.Enemy(width, height, creation_flag, creation_type, center)
            self.enemies.add(en)
            self.surfaces.add(en)

    def add_sprites(self):
        self.surfaces.add(self.player1)
        num_enemies = random.randint(1, self.enemie_count)
        self.add_enemies(0, 0, [0,0], num_enemies)

    def enemy_multiply(self, creation_type, center):
        if creation_type > 2:
            num_enemies = 2 #could make random, a certain number for each size, or certain amount of size 
            self.add_enemies(1, creation_type, center, num_enemies)

    def check_enemies(self):
        if len(self.enemies) == 0:
            self.enemie_count += 1
            self.next_level()

    def en_pro_collisions(self):
        #check for projectile and enemy collision
        for en in self.enemies:
            x = pygame.sprite.spritecollideany(en, self.projects)
            if x != None:
                x.kill()
                en.kill()
                self.enemy_multiply(en.get_creation_type(), en.get_center())
                self.text.set_score(self.text.get_score() + 1)
                self.asteroid_audio()
        if self.game_status == 0: #don't wnat game to go to next level on game over screen
            self.check_enemies()
                #return 1
        #return 0

    def en_plr_collisions(self):
        #check for player collisions
        for en in self.enemies:
            if pygame.sprite.spritecollideany(self.player1, self.enemies, collided=pygame.sprite.collide_mask):
                self.game_status = 1
                self.text.set_score(0)
                self.thrust_flag = 0
                return 1
        return 0
    
    def remove_enemies(self):
        for en in self.enemies:
            en.kill()

    def remove_projectiles(self):
        for proj in self.projects:
            proj.kill()
    
    def remove_sprites(self):
    #clean up sprites on game over
        self.player1.kill()
        self.remove_enemies()
        self.remove_projectiles()
        self.surfaces = pygame.sprite.Group()

    #functions for audio
    def create_sounds(self):
        for file in self.sound_files:
            self.sounds.add_channels(file)
            
    def shoot_audio(self):
        self.sounds.play_audio(0)
    
    def asteroid_audio(self):
        self.sounds.play_audio(2)

    def thrust_audio(self):
        self.sounds.play_audio_loop(1)

    def thrust_audio_pause(self):
        self.sounds.pause_audio(1)

    #functions for high score
    def read_high_score(self):
        high_score_file = open('high_score.txt', "r")
        self.text.set_high_score(int(high_score_file.read()))
        high_score_file.close()

    def write_high_score(self):
        high_score_file = open('high_score.txt', "w")
        high_score_file.write(str(self.text.get_high_score()))
        high_score_file.close()