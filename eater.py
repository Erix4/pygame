from ast import Str
import random
from re import T
import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))#define window
pygame.display.set_caption("Eater")

WHITE = (255, 255, 255)
BLUE = (0, 44, 115)
GREEN = (0, 161, 35)
BLACK = (0,0,0)

FPS = 60
VEL = 5
ACCEL = .1

FOODW, FOODH = 10, 10
DUDEW, DUDEH = 30, 30

class Sprite:
    tbd = False
    #
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
    #
    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)

class Text(Sprite):
    def __init__(self, x, y, w, h, color, text):
        super().__init__(x, y, w, h, color)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = text
    #
    def draw(self):
        textr = self.font.render(self.text, True, self.color)
        WIN.blit(textr, self.rect)

def draw_window(objects):
    WIN.fill(BLUE)
    #
    for obj in objects:
        obj.draw()
    #
    pygame.display.update()

def handle_movement(keys_pressed, dude):
    moved = False
    if keys_pressed[pygame.K_LEFT] and dude.x > 0:
        dude.x -= VEL
        moved = True
    if keys_pressed[pygame.K_RIGHT] and dude.x + dude.width < WIDTH:
        dude.x += VEL
        moved = True
    if keys_pressed[pygame.K_UP] and dude.y > 0:
        dude.y -= VEL
        moved = True
    if keys_pressed[pygame.K_DOWN] and dude.y + dude.height < HEIGHT:
        dude.y += VEL
        moved = True
    return moved

def checkCollision(rect1, rect2):
    return (rect1.x + rect1.width > rect2.x and
            rect1.x < rect2.x + rect2.width and
            rect1.y + rect1.height > rect2.y and
            rect1.y < rect2.y + rect2.height)

def main():
    pygame.init()
    #
    objects = []
    #
    dude = Sprite(20, 70, DUDEW, DUDEH, GREEN)
    objects.append(dude)
    #
    score = 0
    scoreText = Text(20, 20, 100, 50, BLACK, "0")
    objects.append(scoreText)
    #
    counter = 0
    #
    foods = []
    for x in range(100):
        food = Sprite(random.randint(0, WIDTH - FOODW), random.randint(0, HEIGHT - FOODH), FOODW, FOODH, WHITE)
        foods.append(food)
        objects.append(food)
    #
    clock = pygame.time.Clock()
    #
    run = True
    while run:
        clock.tick(FPS)#slow down loop if necessary
        for event in pygame.event.get():#get list of all events
            if event.type == pygame.QUIT:
                run = False
        #
        counter += 1
        if(counter > FPS):
            counter = 0
            food = Sprite(random.randint(0, WIDTH - FOODW), random.randint(0, HEIGHT - FOODH), FOODW, FOODH, WHITE)
            foods.append(food)
            objects.append(food)
        #
        keys_pressed = pygame.key.get_pressed()
        if handle_movement(keys_pressed, dude.rect):
            for food in foods:
                if checkCollision(dude.rect, food.rect):
                    food.tbd = True
                    score += 1
                    scoreText.text = str(score)
            #
            objects = list(filter(lambda obj: not obj.tbd, objects))
            foods = list(filter(lambda obj: not obj.tbd, foods))
        #
        draw_window(objects)
    #
    pygame.quit()

main()