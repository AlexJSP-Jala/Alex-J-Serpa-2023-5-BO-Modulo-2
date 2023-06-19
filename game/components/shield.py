import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP_SHIELD, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET, SPACESHIP
from game.components.bullet import Bullet

class Shield_spaceship(Sprite):
    
    def __init__(self):
        self.image_size = (70, 70)
        self.image = pygame.transform.scale(SPACESHIP_SHIELD, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = 40
        self.image_rect.y = 500
        self.move_left = False
        self.move_right = False
        self.spaceship_speed = 5
        self.move_down = False
        self.move_up = False
        self.bullets = []

    def update(self):
        if self.image_rect is not None:
            if self.move_left and self.image_rect.left > 0:
                self.image_rect.x -= self.spaceship_speed
            if self.move_right and self.image_rect.right < SCREEN_WIDTH:
                self.image_rect.x += self.spaceship_speed
            if self.move_up and self.image_rect.y > 0:
                self.image_rect.y -= self.spaceship_speed
            if self.move_down and self.image_rect.y <= SCREEN_HEIGHT - self.image_rect.height:
                self.image_rect.y += self.spaceship_speed
            if self.image_rect.left <= 0:
                self.image_rect.right = SCREEN_WIDTH
            elif self.image_rect.right >= SCREEN_WIDTH:
                self.image_rect.left = 0

    def shoot(self, x_position_center, y_position):
        self.bullet = Bullet(x_position_center, y_position, BULLET)
        self.bullets.append(self.bullet)
    
    def activate_shield(self):
        self.image = pygame.transform.scale(SPACESHIP_SHIELD, self.image_size)
        self.has_shield = True
    
    def deactivate_shield(self):
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)  
        self.has_shield = False