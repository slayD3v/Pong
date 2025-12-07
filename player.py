import pygame

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 50
PLAYER_BORDER = 20
PLAYER_SPEED = 10

pixelFont = pygame.font.Font("font/slkscr.ttf", 20)

def clamp(value:int, minValue:int, maxValue:int):
    return max(minValue, min(value, maxValue))

class Player():
    rect: pygame.Rect
    window: pygame.Surface
    score: int
    scoreSurface: pygame.Surface

    _left: bool

    def __init__(self, window:pygame.Surface, left:bool):
        self.window = window
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        
        self.score = 0
        self.scoreSurface = pygame.Surface((100, 20))

        self._left = left

        sizeX, sizeY = window.size

        if left:
            self.rect.left = 0
        else:
            self.rect.right = sizeX
        
        self.rect.centery = sizeY//2
        self._left = left        

    def move(self, increment:int):
        sizeY = self.window.size[1]

        applied = self.rect.y + increment
        self.rect.y = clamp(applied, PLAYER_BORDER, sizeY-(PLAYER_HEIGHT+PLAYER_BORDER))

    def update(self):
        sizeX = self.window.size[0]

        scoreText = pixelFont.render(str(self.score), True, (255, 255, 255))
        scoreSizeX = scoreText.size[0]

        self.scoreSurface.fill((0, 0, 0))
        self.scoreSurface.blit(scoreText, (0, 0))
        self.window.blit(self.scoreSurface, (10 if self._left else sizeX-(scoreSizeX+10), 5))

        pygame.draw.rect(
            self.window, 
            (255, 255, 255),
            self.rect
        )