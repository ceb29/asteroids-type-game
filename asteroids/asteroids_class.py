import pygame
from game_classes import Game

class Asteroids(Game):
    def __init__(self, clock_speed, rgb_tuple, sound_files):
        Game.__init__(self,clock_speed, rgb_tuple, sound_files)
        self.thrust_flag = 0
        
    #main game function
    def update(self):
        self.win.fill(self.win_rgb)
        self.text.update_text(self.game_status)
        if self.game_status == 0:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.thrust_on_off()
            self.check_for_collisions()
        else:
            self.remove_sprites()
            self.thrust_audio_pause()
            self.thrust_flag = 0
        pygame.display.flip()
        self.clock.tick(60) 

    #functions for collions between sprites
    def en_pro_collisions(self):
        #check for enemy and projectile collision
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

    def en_plr_collisions(self):
        #check for enemy and player collision
        for en in self.enemies:
            if pygame.sprite.spritecollideany(self.player1, self.enemies, collided=pygame.sprite.collide_mask):
                self.game_over_audio()
                self.game_status = 1
                self.text.set_score(0)
                self.thrust_flag = 0 
    
    #break asteroid up into smaller asteroids
    def enemy_multiply(self, creation_type, center):
        if creation_type > 2:
            num_enemies = 2 #could make random, a certain number for each size, or certain amount of size 
            self.add_enemies(1, creation_type, center, num_enemies)

    #functions for audio
    def shoot_audio(self):
        self.sounds.play_audio(0)
    
    def thrust_audio(self):
        self.sounds.play_audio_loop(1)

    def asteroid_audio(self):
        self.sounds.play_audio(2)

    def game_over_audio(self):
        self.sounds.play_audio(3)

    def thrust_audio_pause(self):
        self.sounds.pause_audio(1)

    #function to handle thrust audio
    def thrust_on_off(self):
        if self.player1.get_thrust_val() == 1 and self.thrust_flag == 0:
            self.thrust_audio()
            self.thrust_flag = 1
        elif self.player1.get_thrust_val() == 0 and self.thrust_flag == 1:
            self.thrust_audio_pause()
            self.thrust_flag = 0

    