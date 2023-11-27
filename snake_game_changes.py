#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:37:28 2022

@author: sharonmoorthy
"""

#SM - Sharon Moorthy
#BL - Bhawna Lachman
#WA - Wardah Anwer
#NY - Nitya Yadav
#Comments refer to the line below them

import pygame
import time
import random

 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
screen_width = 600
screen_height = 400
 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')
#SM -  Change: initializing mixer from pygame to add sounds
pygame.mixer.init 
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 45)
score_font = pygame.font.SysFont("comicsansms", 35)
 
#SM - Change: adjusted the display so that it doesn't show the score if it's zero, only after the first point is gained.
def game_score(score):  
    if score > 0: # SM - Change: only if the score is greater than zero, display the score count.
        value = score_font.render("Score: " + str(score), True, blue)
        screen.blit(value, [0, 0])
    elif score == 0: #SM - Change: if the score is zero, display that the score is zero.
        value = score_font.render("Score: 0", True, blue)
        screen.blit(value, [0, 0])
        game_over = True
    else: # SM - Change: otherwise, the score will be neagitve, so don't display it, and end the game.
        game_over = True 
    
 
 
 
def snake_growth(snake_block, snake_list):
    for x in snake_list:
        #pygame.draw.rect(screen, white, [x[0], x[1], snake_block, snake_block])
        pygame.draw.circle(screen, white, [x[0], x[1]], snake_block)
 
 
def message(text, color):
    msg_type = font_style.render(text, True, color)
    #SM - Change: adjusting the position of the message to be more centered on the screen
    screen.blit(msg_type, [screen_width / 22, screen_height / 3])  
 
 
def game_loop():
    game_over = False
    close_game = False
 
    x1 = screen_width / 2
    y1 = screen_height / 2
 
    x1_movement = 0
    y1_movement = 0
 
    snake_List = []
    snake_length = 1
 
    x_food = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    y_food = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
    #SM - Chamge: adding a second apple for the snake, with the same dimensions.
    x_rotten_apple = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0 
    y_rotten_apple = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while close_game == True:
            screen.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", blue)
            game_score(snake_length - 1)
                
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        close_game = False
                    if event.key == pygame.K_c:
                        game_loop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_movement = -snake_block
                    y1_movement = 0
                elif event.key == pygame.K_RIGHT:
                    x1_movement = snake_block
                    y1_movement = 0
                elif event.key == pygame.K_UP:
                    y1_movement = -snake_block
                    x1_movement = 0
                elif event.key == pygame.K_DOWN:
                    y1_movement = snake_block
                    x1_movement = 0
        
 
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            close_game = True
        x1 += x1_movement
        y1 += y1_movement
        screen.fill(black)
        #pygame.draw.rect(screen, red, [x_food, y_food, snake_block, snake_block])
        pygame.draw.circle(screen, green, (x_food, y_food), 7)
        pygame.display.update
        
        #pygame.draw.rect(screen, green, [x_rotten_apple, y_rotten_apple, snake_block, snake_block])
        pygame.draw.circle(screen, red, (x_rotten_apple, y_rotten_apple), 7)
        pygame.display.update
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List) > snake_length:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_head:
                close_game = True
 
        snake_growth(snake_block, snake_List)
        game_score(snake_length - 1)
 
        pygame.display.update()
 
    
        if x1 == x_food and y1 == y_food:
            x_food = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            y_food = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            snake_length += 1
            #SM - Change: importing the sound file from the folder
            crunch_sound = pygame.mixer.Sound("crunch_sound.mp3") 
            #SM - Change: playing the crunch sound each time the snake eats the apple
            pygame.mixer.Sound.play(crunch_sound) 
            
            
        #change: shrink snake length
        
        if x1 == x_rotten_apple and y1 == y_rotten_apple:
            x_rotten_apple = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            y_rotten_apple = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            #SM - Change: importing sound file from the folder
            crunch_sound = pygame.mixer.Sound("crunch_sound.mp3")
            # SM - Change: playing the crunch sound whenever the snake eats the rotten apple as well.
            pygame.mixer.Sound.play(crunch_sound)
            # BL - Change: reducing the length of the snake by one each time it eats the rotten apple.
            snake_length -= 1
            #BL - Change: removing the x-coordinate of the snake head from the list
            snake_head.remove(x1) 
            # BL - Change: removing the y-coordinate of the snake head from the list
            snake_head.remove(y1) 
            #BL - Change: removing the appended snake_heads from the snake list each time it eats the rotten apple    
            snake_List.remove(snake_head)  
           
         
        # BL - Change: if the length of the snake becomes zero, end the game   
        if snake_length - 1 < 0: 
            close_game = True
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
game_loop()









