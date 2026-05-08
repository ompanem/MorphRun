import pygame
from form import Form
from form import FORM_IMAGES_MULTIPLIER
from form import FORM_LOADED_IMAGES


class Player:
    def __init__(self, x: int, y: int, form: Form):
        self.x = x
        self.y = y
        self.form = form
        #for when player dies
        self.originalX = x
        self.originalY = y
        self.image = FORM_LOADED_IMAGES[form]
        self.dead = False
        self.won = False
        #velY is a instance var because I need to apply gravity every frame so it can't reset locally
        self.velY = 0
        self.onGround = True

        imageWidth = self.image.get_width()
        imageHeight = self.image.get_height()
        self.gravity = 0.8
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def update(self, keyPressed: pygame.key.ScancodeWrapper, platforms, enemies):
        
        velX = 0
        if(keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d]):
            velX = 5
        if(keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a]):
            velX = -5
        #Only jump when its on the ground
        if(keyPressed[pygame.K_SPACE] and self.onGround):
            self.velY = -15
            self.onGround = False
        
        self.x+=velX
        self.rect.x = self.x

        #Horizontal collision checks before vertical to prevent teleportation glitches
        for platform in platforms:
            if(platform.intersects(self)):
                if(self.form == Form.BRUTE and platform.breakable and platform.alive):
                    platform.alive = False
                else:                  
                    if(velX>0):
                      self.x = platform.rectangle.left - self.image.get_width()
                      self.rect.x = self.x
                    elif(velX<0):
                      self.x = platform.rectangle.right
                      self.rect.x = self.x

        
        #Keep the previous y position to show direction from which player was coming (for enemy collisions)
        prev_bottom = self.y + self.image.get_height()
        self.velY+=self.gravity
        self.y+=self.velY
        self.rect.y = self.y
     
        for platform in platforms:
            #positive velY means object moving downward so check for that
            if(platform.intersects(self)):
                if(platform.goal):
                   self.won = True
                if(self.form == Form.BRUTE and platform.alive and platform.breakable):
                  #prevent resetting timer 
                  if(platform.break_timer == -1):
                    platform.break_timer = 20
                  if(self.velY>0):
                    self.y = platform.rectangle.top - self.image.get_height()
                    self.rect.y = self.y
                    self.velY = 0
                    self.onGround = True
                else:
                  if(self.velY>0):
                    self.y = platform.rectangle.top-self.image.get_height()
                    self.rect.y = self.y
                    self.velY = 0   
                    self.onGround = True
                    
                  elif(self.velY<0):
                    self.y = platform.rectangle.bottom
                    self.rect.y = self.y
                    self.velY = 0
         
        for enemy in enemies:
            if(enemy.intersects(self) and enemy.alive):
                if(prev_bottom<=enemy.y+10):
                    enemy.alive = False
                    self.morph(enemy.form)
                else:
                    self.dead = True
        if(self.y>600 or self.x<0 or self.x>800):
           self.dead = True
    
    def morph(self, form):
        multiplier = FORM_IMAGES_MULTIPLIER[form]
        self.form = form
        self.image = FORM_LOADED_IMAGES[form]
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    

    def draw(self, screen):
        screen.blit(self.image, (int(self.x),int(self.y)))