import pygame
import random

pygame.init()

blocks = []
current_block = None
score = 0
misses = 0
first_start = True
running = True
position = 1

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, 600))
pygame.display.set_caption('Tower Blocks')

ALLOWWED_X = 525

CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont('Times New Roman', 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BACKGROUND_IMAGE = pygame.image.load('background_image.jpg')

BLOCK_SIZE = 50
BLOCK_SPEED = 5

BLOCK_IMAGE_PATH = 'block_image.png'
BLOCK_IMAGE = pygame.image.load(BLOCK_IMAGE_PATH).convert_alpha()
BLOCK_IMAGE = pygame.transform.scale(BLOCK_IMAGE, (BLOCK_SIZE, BLOCK_SIZE))

class Block:
    def __init__(self, x, y, size, image_path):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (size, size))
        self.speed = BLOCK_SPEED
        self.direction = 1
        self.moving = True  
        self.droped = False

    def move(self):
        if self.moving:
            self.x += self.speed * self.direction
            if self.x < 0 or self.x + self.size > WINDOW_WIDTH:
                self.direction *= -1
            
    def start_moving(self):
        self.moving = True

    def stop_moving(self):
        self.moving = False

    def drop(self):
        self.stop_moving()
        self.speed = BLOCK_SPEED * 2  
        self.direction = 0  
        if self.y <= WINDOW_HEIGHT - (BLOCK_SIZE * position):
            self.y += self.speed 
            
    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_block is not None:
                    print("SPACE PRESSED")
                    current_block.speed = BLOCK_SPEED
                    current_block.droped = True
                    if current_block.x >= 460 and current_block.x <= 540:
                        position += 1
                        score += 1 
                        blocks.append(current_block)       
                    else:
                        misses += 1 
    if score == 10:
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        you_won_text = game_over_font.render('You won', True, (255, 255, 255))
        WINDOW.blit(you_won_text, (WINDOW_WIDTH/2 - you_won_text.get_width()/2, WINDOW_HEIGHT/2 - you_won_text.get_height()/2))
        pygame.display.update()
        pygame.time.wait(5000) 
        running = False
    if misses == 3:
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        you_lost_text = game_over_font.render('You lost', True, (255, 255, 255))
        WINDOW.blit(you_lost_text, (WINDOW_WIDTH/2 - you_lost_text.get_width()/2, WINDOW_HEIGHT/2 - you_lost_text.get_height()/2))
        pygame.display.update()
        pygame.time.wait(5000) 
        running = False
    if current_block is None:
        print("CURRENT_BLOCK IS NONE")
        x = (WINDOW_WIDTH - BLOCK_SIZE )/ 2
        y = 0  
        size = BLOCK_SIZE 
        image_path = 'block_image.png'  
        current_block = Block(x, y, size, image_path)
    if current_block.droped is True:
        current_block.drop()
            
        if current_block.y == WINDOW_HEIGHT - (BLOCK_SIZE * position):
            current_block = None
        
    
    if current_block is not None:
        current_block.move()
        WINDOW.blit(BACKGROUND_IMAGE, (0, 0))
        first_block  = Block((WINDOW_WIDTH) / 2, (WINDOW_HEIGHT - BLOCK_SIZE), size, image_path)
        blocks.append(first_block)
    
    for block in blocks:
        block.draw()
    if current_block is not None:
        current_block.draw()
    
        score_text = FONT.render(f'Score: {score}', True, WHITE)
        WINDOW.blit(score_text, (10, 10))
        misses_text = FONT.render(f'Misses: {misses}', True, RED)
        WINDOW.blit(misses_text, (10, 45))
        pygame.display.update()
        CLOCK.tick(60)

    with open('scores.txt', 'a') as file:
        file.write(str(score) + '\n')