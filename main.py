import random 
import sys
import pygame
from pygame.locals import * 

FPS = 40
SCREENWIDTH = 500 
SCREENHEIGHT = 600 
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.85 
GAME_pictures = {}
PLAYER = 'gallery/pictures/bird.png'
BACKGROUND = 'gallery/pictures/background.png'
PIPE = 'gallery/pictures/pipe.png'

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_pictures['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_pictures['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0)
    basex = 0
    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_pictures['background'], (0, 0))    
                SCREEN.blit(GAME_pictures['player'], (playerx, playery))# on x and y axis    
                SCREEN.blit(GAME_pictures['message'], (messagex,messagey ))# on x and y axis    
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)# on x axis
    playery = int(SCREENWIDTH/2)# on y axis
    basex = 0

    newPipe1 = getRandomPipe()# for pipes coming on screen 
    newPipe2 = getRandomPipe()
# my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
# my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    pipeVelX = -4
    playerVelY = -9 #weight of bird 
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1 #gravitational force 

    playerFlapAccv = -8 
    playerFlapped = False 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE ):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            gameOverScreen(score)
            return     

        playerMidPos = playerx + GAME_pictures['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_pictures['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1#score
                print(f"Your score is ",score) #it will print score in thonny output
                
        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_pictures['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        
# move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

# Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5 :
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

# if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_pictures['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
# Lets blit our pictures now
        SCREEN.blit(GAME_pictures['background'], (0, 0))#background
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_pictures['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_pictures['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_pictures['base'], (basex, GROUNDY))#ground &base
        SCREEN.blit(GAME_pictures['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_pictures['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:#sizing of numbers
            SCREEN.blit(GAME_pictures['numbers'][digit], (Xoffset, SCREENHEIGHT*0.14))
            Xoffset += GAME_pictures['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def gameOverScreen(score):
    """Display the Game Over screen."""
    # Clear the screen and display the "Game Over" message
    SCREEN.blit(GAME_pictures['background'], (0, 0))  # Background
    gameOverMessage = pygame.image.load('gallery/pictures/game_over.png').convert_alpha()  # Make sure you have this image
    messageX = int((SCREENWIDTH - gameOverMessage.get_width()) / 2)
    messageY = int(SCREENHEIGHT * 0.4)  # Position the message near the middle
    SCREEN.blit(gameOverMessage, (messageX, messageY))
    
    # Display the score
    scoreMessage = f"Score: {score}"
    font = pygame.font.SysFont('Arial', 30)
    scoreText = font.render(scoreMessage, True, (255, 255, 255))
    scoreX = int((SCREENWIDTH - scoreText.get_width()) / 2)
    scoreY = messageY + gameOverMessage.get_height() + 20
    SCREEN.blit(scoreText, (scoreX, scoreY))
    
    pygame.display.update()

    # Wait for player input (Space or Enter to restart, Escape to quit)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_RETURN:
                    return  # Restart the game
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

#function for collision with pipes
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        return True
#collision with upper pipe    
    for pipe in upperPipes:
        pipeHeight = GAME_pictures['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_pictures['pipe'][0].get_width()):
            return True
#collision with lower pipe    
    for pipe in lowerPipes:
        if (playery + GAME_pictures['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_pictures['pipe'][0].get_width():
            return True

    return False
#pipes will come in random manner 
def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """#settings of pipe
    pipeHeight = GAME_pictures['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_pictures['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_pictures['numbers'] = ( #pictures of numbers
        pygame.image.load('gallery/pictures/0.png').convert_alpha(),pygame.image.load('gallery/pictures/1.png').convert_alpha(),
        pygame.image.load('gallery/pictures/2.png').convert_alpha(),pygame.image.load('gallery/pictures/3.png').convert_alpha(),
        pygame.image.load('gallery/pictures/4.png').convert_alpha(),pygame.image.load('gallery/pictures/5.png').convert_alpha(),
        pygame.image.load('gallery/pictures/6.png').convert_alpha(),pygame.image.load('gallery/pictures/7.png').convert_alpha(),
        pygame.image.load('gallery/pictures/8.png').convert_alpha(),pygame.image.load('gallery/pictures/9.png').convert_alpha(),
    )

    GAME_pictures['message'] =pygame.image.load('gallery/pictures/message.png').convert_alpha()
    GAME_pictures['base'] =pygame.image.load('gallery/pictures/base.png').convert_alpha()#picture of base
    GAME_pictures['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), #picture of pipe
    pygame.image.load(PIPE).convert_alpha()
    )

    GAME_pictures['background'] = pygame.image.load(BACKGROUND).convert()#picture of background
    GAME_pictures['player'] = pygame.image.load(PLAYER).convert_alpha()#picture of player

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function
