import pygame

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int], breakable: bool):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rectangle = pygame.Rect(x,y, width, height)
        self.breakable = breakable
        self.break_timer = -1
        self.alive = True
        self.goal = False
    def update(self):
        if(self.break_timer>0):
            self.break_timer-=1
        elif(self.break_timer == 0):
            self.alive = False
    def draw(self, screen):
        if(self.alive):          
            pygame.draw.rect(screen, self.color, self.rectangle)
     
    def intersects(self, user) -> bool:
        if(self.alive): 
            return pygame.Rect.colliderect(self.rectangle, user.rect)
        return False