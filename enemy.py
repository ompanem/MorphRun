import pygame
from game_platform import Platform
import random
from form import Form
from form import FORM_LOADED_IMAGES
class Enemy:
    def __init__(self, x: int, form: Form, platform: Platform):
        self.x = x
        self.form = form
        self.image = FORM_LOADED_IMAGES[form]
        self.platform = platform
        if(self.x < platform.x or self.x > platform.x + platform.width):
            self.x = random.randint(platform.x, platform.width - self.image.get_width())
        self.y = platform.y - self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.velX = 5
        self.alive = True

    
    def update(self):
        if(self.alive):
            self.x+=self.velX
            self.rect.x = self.x
            #simple movement for now left to right
            if(self.x + self.image.get_width()>=self.platform.x + self.platform.width):
                self.velX *= -1
            elif(self.x<=self.platform.x):
                self.velX*=-1

        
    
    def draw(self, screen):
        if(self.alive):
            screen.blit(self.image, (int(self.x), int(self.y)))

    def intersects(self, user):
        return pygame.Rect.colliderect(self.rect, user.rect)
        