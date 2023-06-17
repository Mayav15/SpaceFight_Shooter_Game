import pygame
import os
pygame.font.init()  #For text and fonts in game
pygame.mixer.init() #Starts sound asspect of pygame

WIDTH, HEIGHT = 900, 500
#Width and height for the window screen, i.e. the screen on which the game will be played.

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40
#Width and height of the images of spaceships.
#Storing constant values gloablly in variables to make sure we can use them anywhere in the code.

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#WIN is the variable name for the window

pygame.display.set_caption("1st game using pygame")
#This is to set the title of the window of the game

WHITE = (255, 255, 255)
LBLUE = (0, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
#These are the values for colours that we will most likely be using everywhere.

BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
# BORDER = pygame.Rect(x,y,width,height)

FPS = 60
#Frames per Seconds, speed for refreshment of screen.

VEL = 5
# The velocity is the number of pixels the character/rectangle/image will move when any key is pressed.

BULLET_VEL = 7

MAX_BULLETS = 5

YELLOW_HIT = pygame.USEREVENT + 1   # Creating a new event to check for collision and then making changes wherever necessary
RED_HIT = pygame.USEREVENT + 2      # Creating a new event. If both were +1 then they would have been the same event with the same number represeting them

Y_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
Y_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(Y_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)
R_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
R_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(R_SPACESHIP_IMAGE,(50,40)), 270)
#os.path.join() used because depending on what operating system you are on, directory separator may be different. This will handle it.
#pygame.transform.rotate is to rotate the images anticlockwize by x degrees
#pygame.transform.scale is to scale the image size to desired dimensions

SPACE =pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH,HEIGHT))

HEALTH_FONT = pygame.font.SysFont("impact",40)
WINNER_FONT = pygame.font.SysFont('serif',100)

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #we pass red and yellow rectangles here to get the positions and to track their movements and collisions, etc.
    
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, LBLUE, BORDER)

    red_health_text = HEALTH_FONT.render("Health: "+str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10, 20))
    WIN.blit(yellow_health_text,(10, 20))

    WIN.blit(Y_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(R_SPACESHIP,(red.x,red.y))
    #.blit() is used when you want to draw a surface on the screen.
    #The order in which we draw things matter. so if we fill after using blit, we will not see the image.
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    # This is drawing all the bullets for yellow and red ships. The bullets are simply rectangles.

    pygame.display.update()
    #You will have to update the display after doing changes in pygame, otherwise the changes wont show in window

def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+10:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL<900-SPACESHIP_HEIGHT:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL>0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL<500-SPACESHIP_WIDTH:
        red.y += VEL

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL<BORDER.x-SPACESHIP_HEIGHT:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL<500-SPACESHIP_WIDTH:
        yellow.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    #This will move bullets, handle collisions, remove bullets when they are off screen or when they collide with other characters.
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.x>WIDTH:
            yellow_bullets.remove(bullet)
        if red.colliderect(bullet):
        # a.colliderect(b) checks if rectangle representing a has collided with rectangle representing b.
            
            pygame.event.post(pygame.event.Event(RED_HIT))  
            # Making a new event saying the red player was hit

            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if bullet.x<0:
            red_bullets.remove(bullet)
        if yellow.colliderect(bullet):
        # a.colliderect(b) checks if rectangle representing a has collided with rectangle representing b.
            
            pygame.event.post(pygame.event.Event(YELLOW_HIT))  
            # Making a new event saying the red player was hit
            
            red_bullets.remove(bullet)

def draw_winner(text):
    win_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(win_text,(WIDTH//2-(win_text.get_width()//2),HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(5000)
    #The time for which the text is displayed on screen

def main():
    # Usually the main function is used for redrawing the window, checking for ccollisions, updating the score, etc. Usually a loop.

    red = pygame.Rect(675,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(225,250,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    #rectangle =pygame.Rect(x,y,width,height)
    #The rectangles are to keep track of position of the spaceships in the game and also to check for collisions, stc.
    
    red_bullets = []
    yellow_bullets = []

    red_health, yellow_health= 10, 10

    clock = pygame.time.Clock()
    #Defining a clock object to keep track of how fast the screen is to be refreshed.
    
    run = True
    while run:
        clock.tick(FPS)
        #.tick(FPS) makes sure that your game never goes above the FPS mentioned, so it will run the same on all computers.
        
        for event in pygame.event.get():
            #This is a loop where we go through all possible events in the game.
            #pygame.event.get() gives you list of all events in game
            
            if event.type==pygame.QUIT:
                run = False
                #In case the user quits the game
                
                pygame.quit()
                #Quits pygame for us and closes the window
        
            if event.type==pygame.KEYDOWN:
                #This is the event that a key is pressed downwards

                if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:   #Left control
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key==pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:   #Right control
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        win_text=""
        if red_health<=0:
            win_text = "Yellow Wins!"

        if yellow_health<=0:
            win_text = "Red Wins!"

        if win_text != "":
            draw_winner(win_text)
            break

        #MOVEMENT FOR RED SPACESHIP
        keys_pressed = pygame.key.get_pressed()
        #Everytime the loop reaches this line, it will tell us what keys are currentl being pressed down.
        
        handle_red_movement(keys_pressed,red)
        handle_yellow_movement(keys_pressed, yellow)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        #Calling the function to make sure we are applying changes. You can also make changes in main function.

    main()
    #This means the game retstarts after a player wins and the display text is removed


if __name__ == "__main__":
    main()