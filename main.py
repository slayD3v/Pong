import pygame, random

# Setup
pygame.init()

from player import Player, PLAYER_SPEED, PLAYER_WIDTH

windowSize = width, height = (400, 400)
halfHeight = height//2

screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Pong")

clock = pygame.Clock()

# Game State
aiOpponent = False

running = True

playerA = Player(screen, True)
playerB = Player(screen, False)

hitSfx = pygame.mixer.Sound("sound/hit.wav")
resetSfx = pygame.mixer.Sound("sound/reset.wav")

ballRect = pygame.Rect(0, 0, 20, 20)

ballSpeedX = 0
ballSpeedY = 0

def clamp(value:int, minValue:int, maxValue:int):
    return max(minValue, min(value, maxValue))

def resetBall():
    global ballSpeedX, ballSpeedY

    ballRect.center = (width//2, height//2)
    ballSpeedX = 7#random.randint(3, 7) * random.choice([-1, 1])
    ballSpeedY = 6#random.randint(3, 6) * random.choice([-1, 1])

resetBall()

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        playerA.move(-PLAYER_SPEED)
    
    if keys[pygame.K_s]:
        playerA.move(PLAYER_SPEED)

    if not aiOpponent:
        if keys[pygame.K_UP]:
            playerB.move(-PLAYER_SPEED)
        
        if keys[pygame.K_DOWN]:
            playerB.move(PLAYER_SPEED)
        
    # Check if it collides
    if ballRect.top<=0 or ballRect.bottom>=height:
        ballSpeedY *= -1

    if ballRect.colliderect(playerA.rect):
        ballSpeedX *= -1
        ballRect.left = PLAYER_WIDTH+1
        hitSfx.play()
    
    if ballRect.colliderect(playerB.rect):
        ballSpeedX *= -1
        ballRect.right = width - (PLAYER_WIDTH+1)
        hitSfx.play()

    ballRect.x += ballSpeedX
    ballRect.y += ballSpeedY

    # AI
    if ballRect.x>=(width*.6) and aiOpponent:
        playerB.move( clamp(ballRect.y-playerB.rect.y, -5, 5) )

    # Check if out of bounds
    if (ballRect.x<-10 or ballRect.x>width):
        if (ballRect.x<-10):
            playerB.score += 1
        elif ballRect.x>width:
            playerA.score += 1

        resetSfx.play()
        resetBall()

    screen.fill((0, 0, 0)) # Clear Screen

    playerA.update()
    playerB.update()

    pygame.draw.circle(
        screen, 
        (255, 255, 255), 
        ballRect.center, 
        ballRect.width//2
    )
    pygame.display.flip()

    clock.tick(60)