import pygame
from pygame.sprite import Sprite

from game.utils.constants import  SCREEN_WIDTH, BULLET_ENEMY
from game.components.bullet import Bullet

class Enemy(Sprite):

    def __init__(self, x_position, y_position, figure):
        super().__init__()
        self.x_position = x_position
        self.y_position = y_position
        self.image_size = (40, 50)
        self.image = pygame.transform.scale(figure, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x_position
        self.image_rect.y = y_position
        self.move_left = False
        self.move_right = False
        # Enemy ship movement configuration
        self.spaceship_enemy_speed = 5
        self.enemy_direction = 1
        self.bullets = []

    def update(self):
        # Update enemy ship position
        #if self.image_rect is None:
        if self.image_rect is not None:
            if self.image_rect.left <= 0 or self.image_rect.right >= SCREEN_WIDTH:
                self.enemy_direction *= -1  # Reverse direction if it reaches the lateral limits.
            self.image_rect.x += self.enemy_direction * self.spaceship_enemy_speed
    
    def shoot(self, x_position_center, y_position):
        self.bullet = Bullet(x_position_center, y_position, BULLET_ENEMY)
        self.bullets.append(self.bullet)
    
            