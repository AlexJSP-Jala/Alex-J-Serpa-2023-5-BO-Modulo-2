import pygame
from pygame.sprite import Sprite
from game.utils.constants import  SCREEN_HEIGHT



#bullets = []

class Bullet(Sprite):
    
    def __init__(self,x_position_center, y_position, image_bullet):
        self.x_position_center = x_position_center
        self.y_position = y_position
        self.image_size = (10, 10)
        self.image = pygame.transform.scale(image_bullet, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = x_position_center
        self.image_rect.bottom = y_position
        self.impact = 0
        self.deaths = 0
        #self.global_game_over = False
        
        
        #self.bullet_speed = 10

    def update(self, speed_bullet):
        self.image_rect.y -= speed_bullet
    
    def shoot_eliminate(self, enemy, bullets, speed_bullet, bullet_lethality):
        for bullet in bullets:
            bullet.update(speed_bullet)
            if bullet.image_rect.top <= 0 or bullet.image_rect.bottom >= SCREEN_HEIGHT: 
                bullets.remove(bullet)

            if enemy.image_rect is not None and bullet.image_rect.colliderect(enemy.image_rect):
                bullets.remove(bullet)
                self.impact += 1
                if self.impact>= bullet_lethality:
                    self.deaths += 1
                    enemy.image_rect = None  
                    
                    
                    
            

    



