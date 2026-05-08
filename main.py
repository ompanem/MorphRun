import pygame
from player import Player
from game_platform import Platform
from enemy import Enemy
from form import Form
from form import load_form_images
from form import FORM_LOADED_IMAGES
from gamestate import GameState
import level_loader


#initialize
pygame.init()
#Create the screen 
dimensions = (800,600)
screen = pygame.display.set_mode(dimensions)
load_form_images()
#Title and Caption
pygame.display.set_caption("Morph Run")

#Player 
platforms, enemies, playerX, playerY = level_loader.load_level("levels/level1.txt")
form = FORM_LOADED_IMAGES[Form.BASE]
gameState = GameState.MENU
title_font = pygame.font.Font(None, 50)
text_font = pygame.font.Font(None, 50)

#colors
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
ORANGE = (255,165,0)   
YELLOW = (255,255,0)
#Game Loop
running = True
user = Player(playerX, playerY, Form.BASE)
clock = pygame.time.Clock() #How fast the game loop is running

#currentLevel
currentLevel = 1
def reset_level():
        global platforms, enemies, user
        platforms, enemies, playerX, playerY = level_loader.load_level(f"levels/level{currentLevel}.txt")
        user = Player(playerX, playerY, Form.BASE)
        user.dead = False

while(running):
    clock.tick(60)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_r):
                if(gameState == GameState.PLAYING):
                    user.dead = True
                elif gameState == GameState.DEAD:
                    user.dead = True
                    reset_level()
                    gameState = GameState.PLAYING
            if(event.key == pygame.K_SPACE):
                if gameState == GameState.MENU:
                    gameState = GameState.PLAYING
                elif gameState == GameState.WIN:
                    try:
                        currentLevel+=1
                        platforms, enemies, playerX, playerY = level_loader.load_level(f"levels/level{currentLevel}.txt")
                        user = Player(playerX, playerY, Form.BASE)
                        gameState = GameState.PLAYING
                    except FileNotFoundError:
                        gameState = GameState.FINISHED
            if(event.key == pygame.K_p):
                if gameState == GameState.FINISHED:
                    currentLevel = 1
                    reset_level()
                    gameState = GameState.MENU
    keyPressed = pygame.key.get_pressed()
    screen.fill((0,0,0))
    if(gameState == GameState.MENU):
        title = title_font.render("Morph RUN", True, WHITE)
        line1 = text_font.render("Press SPACE to start.", True, WHITE)
        line2 = text_font.render("Jump on enemies to transform", True, WHITE)
        line3 = text_font.render("Press R to reset", True, WHITE)
        screen.blit(title, (300,150))
        screen.blit(line1, (250,250))
        screen.blit(line2, (150,300))
        screen.blit(line3, (250,350))
    elif gameState == GameState.PLAYING:
        if user.dead:
            gameState = GameState.DEAD
        user.update(keyPressed, platforms, enemies)        

        for p in platforms:
            p.update()
            #Will be dead if
            if(p.alive):
                p.draw(screen)
                if(user.won):
                    gameState = GameState.WIN
          
        user.draw(screen)
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)
   
    
    elif gameState == GameState.DEAD:
         msg = title_font.render("You Died!", True, RED)
         retryMsg = text_font.render("Press R to retry", True, WHITE)
         screen.blit(msg, (300,200))
         screen.blit(retryMsg, (290,300))

    elif gameState == GameState.WIN:
        msg = title_font.render("YOU WIN! ", True, YELLOW)
        nextLvlMsg = text_font.render("PRESS SPACE for next level!", True, WHITE)
        screen.blit(msg, (300,200))
        screen.blit(nextLvlMsg, (290,300))
    elif gameState == GameState.FINISHED:
        msg = title_font.render("YOU BEAT THE GAME!", True, YELLOW)
        thanks = text_font.render("Thanks for playing!", True, WHITE)
        playAgainMsg = text_font.render("Press P to play again!", True, WHITE)
        screen.blit(msg, (180,200))
        screen.blit(thanks, (240,280))
        screen.blit(playAgainMsg, (220,350))
  
  
    pygame.display.flip()