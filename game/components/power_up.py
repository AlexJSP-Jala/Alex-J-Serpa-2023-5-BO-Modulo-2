import pygame
from pygame.sprite import Sprite


class Power_up(Sprite):

    def __init__(self, x_position, y_position, figure):
        #Shield image
        super().__init__()
        self.image_size_shield = (20, 20)
        self.shield_image = pygame.transform.scale(figure, self.image_size_shield)
        self.shield_image_rect = self.shield_image.get_rect()
        self.shield_image_rect.x = x_position
        self.shield_image_rect.y = y_position

        
    def update(self):
        self.shield_image_rect.y += 3
    