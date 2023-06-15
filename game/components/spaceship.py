import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT

# casi Todo en pygame es un objeto
# Un personaje en mi juego es un objeto (instancia de algo)
# La nave (spaceship) es un personaje => necesito una clase



# SpaceShip es una clase derivada (hija) de Sprite

# spaceship tiene una "imagen"
class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = 40
        self.image_rect.y = 500
        self.move_left = False
        self.move_right = False
        self.spaceship_speed = 5
        self.move_down = False
        self.move_up = False
        

    def update(self):
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




