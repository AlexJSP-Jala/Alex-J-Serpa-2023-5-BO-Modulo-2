import pygame
from pygame.sprite import Sprite
from game.utils.constants import  SCREEN_HEIGHT


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
        
    
    def update_bullet(self, bullets, speed_bullet):
        for bullet in bullets:
            #bullet.update(speed_bullet)
            bullet.image_rect.y -= speed_bullet
            if bullet.image_rect.top <= 0 or bullet.image_rect.bottom >= SCREEN_HEIGHT: 
                bullets.remove(bullet)

            
                    
       
                    
                    
                    
                    
            

    



