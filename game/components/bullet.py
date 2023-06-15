import pygame
from pygame.sprite import Sprite

from game.utils.constants import BULLET

bullets = []

class Bullet(Sprite):
    
    def __init__(self,x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.image_size = (10, 10)
        self.image = pygame.transform.scale(BULLET, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = x_position
        self.image_rect.bottom = y_position
        self.bullet_speed = 10

    def update(self):
        self.image_rect.y -= self.bullet_speed 



