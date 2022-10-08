from cmath import sqrt
import matplotlib.pyplot as plt
import random
import pygame
import numpy as np
from brain import Brain

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))#define window
pygame.display.set_caption("Eater")

WHITE = (255, 255, 255)
BLUE = (0, 44, 115)
GREEN = (0, 161, 35)
BLACK = (0,0,0)

FPS = 60
VEL = 15

FOODW, FOODH = 10, 10
DUDEW, DUDEH = 30, 30

FOOD_ENERGY = 20
FOOD_NUM = 500
TIME_CAP = 1000
SIGHT_MAX = 10

GENE_NUM = 20
CREATURE_NUM = 500

SHOW_BEST = True

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

class Creature(Sprite):
    def __init__(self, x, y, w, h, color, cr_id, *args):
        super().__init__(x, y, w, h, color)
        self.id = cr_id
        #
        if(len(args) < 2):
            self.brain = Brain(GENE_NUM)
            self.sight = random.randint(1, SIGHT_MAX)
        else:
            self.brain = Brain(args[0], args[1])
            self.sight = args[2]
        #
        self.start = [x, y]
        self.viewBox = pygame.Rect(x - (self.sight * w), y - (self.sight * h), w * (1 + (2 * self.sight)), h * (1 + (2 * self.sight)))
        #
        self.energy = 100
        self.score = 0
    #
    def update(self, foods, ticks):
        inputs = self.getInputs(foods, ticks)
        #
        outputs = self.brain.forward(inputs)
        #
        self.energy -= 1
        #
        self.rect.x += VEL * outputs[0]
        self.rect.y += VEL * outputs[1]
        #
        #match move:#do nothing if 4
        #    case 0:
        #       self.rect.x -= VEL
        #    case 1:
        #        self.rect.y -= VEL
        #    case 2:
        #        self.rect.x += VEL
        #    case 3:
        #        self.rect.y += VEL
    #
    def reset(self, set_score=True):
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
        #
        self.viewBox.x = self.start[0] - self.rect.width
        self.viewBox.y = self.start[1] - self.rect.height
        #
        self.energy = 100
        if(set_score):
            self.score = 0
    #
    def getInputs(self, foods, ticks):
        inputs = [0, 0, 0, 0, 0]
        for food in foods:
            if checkCollision(self.viewBox, food.rect):
                if (food.rect.y + food.rect.height > self.rect.y and food.rect.y < self.rect.y + self.rect.height):
                    if(food.rect.x < self.rect.x):
                        inputs[0] += (self.rect.x - (food.rect.x + food.rect.width)) / (self.rect.width * self.sight)
                    else:
                        inputs[2] += (food.rect.x - (self.rect.x + self.rect.width)) / (self.rect.width * self.sight)
                elif (food.rect.x + food.rect.width > self.rect.x and food.rect.x < self.rect.x + self.rect.width):
                    if(food.rect.y < self.rect.y):
                        inputs[1] += (self.rect.y - (food.rect.y + food.rect.height)) / (self.rect.height * self.sight)
                    else:
                        inputs[3] += (food.rect.y - (self.rect.y + self.rect.height)) / (self.rect.height * self.sight)
        #
        inputs[4] = ticks / TIME_CAP
        #
        for x in range(len(inputs)):
            inputs[x] = np.tanh(inputs[x])
        #
        return inputs

def draw_window(objects):
    WIN.fill(BLUE)
    #
    for obj in objects:
        obj.draw()
    #
    pygame.display.update()

def checkCollision(rect1, rect2):
    return (rect1.x + rect1.width > rect2.x and
            rect1.x < rect2.x + rect2.width and
            rect1.y + rect1.height > rect2.y and
            rect1.y < rect2.y + rect2.height)

def main():
    pygame.init()
    #
    bests = []
    avgs = []
    #
    species = [[]]
    #
    objects = []
    #
    status = Text(20, 20, 200, 50, BLACK, "Loading")
    objects.append(status)
    draw_window(objects)
    #
    cr_id = 0
    creatures = []
    for x in range(CREATURE_NUM):
        cr = Creature(WIDTH / 2, HEIGHT / 2, DUDEW, DUDEH, GREEN, cr_id)
        creatures.append(cr)
        cr_id += 1
    #
    cr_num = 0
    high_cr = 0
    gen = 0
    sum = 0
    #
    clock = pygame.time.Clock()
    #
    mode = 0 #0 = set up, 1 = calc cr, 2 = process cr, 3 = show best, 4 = mutate
    #
    print("Starting...", end="")
    #
    run = True
    while run:
        for event in pygame.event.get():#get list of all events
            if event.type == pygame.QUIT:
                run = False
        #
        match mode:
            case 0:
                foods = []
                for x in range(FOOD_NUM):#create foods
                    food = Sprite(random.randint(0, WIDTH - FOODW), random.randint(0, HEIGHT - FOODH), FOODW, FOODH, WHITE)
                    foods.append(food)
                #
                ticks = 0
                #
                mode = 1
            case 1:
                #status.text = "Gen " + str(gen) + ", Calc cr " + str(cr_num)
                #draw_window(objects)
                print("\r", end="")
                print("Gen " + str(gen) + ", Calc cr " + str(cr_num), end="\r")
                #
                creatures[cr_num].update(foods, ticks)
                #
                creatures[cr_num].energy -= 1
                ticks += 1
                #
                for food in foods:
                    if checkCollision(creatures[cr_num].rect, food.rect):
                        food.tbd = True
                        creatures[cr_num].score += 1
                        creatures[cr_num].energy += FOOD_ENERGY
                #
                foods = list(filter(lambda obj: not obj.tbd, foods))
                #
                #if(ticks == int(TIME_CAP / 2)):
                #    for food in foods:
                #        food.rect.x = (food.rect.x / 2) + WIDTH / 2
                #
                if(creatures[cr_num].energy < 0 or ticks > TIME_CAP or 
                creatures[cr_num].rect.x < 0 or 
                creatures[cr_num].rect.x > WIDTH or
                creatures[cr_num].rect.y < 0 or
                creatures[cr_num].rect.y > HEIGHT):
                    #
                    sum += creatures[cr_num].score
                    if creatures[cr_num].score > high_cr: 
                        high_cr = creatures[cr_num].score
                    cr_num += 1
                    #
                    if(cr_num == len(creatures)):
                        mode = 2
                    else:
                        mode = 0
            case 2:
                creatures.sort(key = lambda cr: cr.score, reverse=True)
                #
                print()
                bests.append(creatures[0].score)
                print("best:", creatures[0].id, "mutation", int(creatures[0].id / CREATURE_NUM), "with", creatures[0].score, "vs max:", high_cr, ", avg: ", (sum / CREATURE_NUM))
                avgs.append(sum / CREATURE_NUM)
                #
                print("sight:", creatures[0].sight)
                print(creatures[0].brain)
                #
                for cr in creatures:
                    species[len(species) - 1].append(cr.id % CREATURE_NUM)
                #
                #for cr in creatures:
                    #print(cr.id, end=", ")
                #print()
                #
                if(SHOW_BEST):
                    foods = []
                    for x in range(FOOD_NUM):#create foods
                        food = Sprite(random.randint(0, WIDTH - FOODW), random.randint(0, HEIGHT - FOODH), FOODW, FOODH, WHITE)
                        #food = Sprite((x % int(sqrt(FOOD_NUM))) * (WIDTH - FOODW), int(x / int(sqrt(FOOD_NUM))) * (WIDTH - FOODW), FOODW, FOODH, WHITE)
                        foods.append(food)
                        objects.append(food)
                    #
                    creatures[0].reset(False)
                    ticks = 0
                    #
                    objects.append(creatures[0])
                    #
                    mode = 3
                else:
                    mode = 4
                #
            case 3:
                clock.tick(FPS)
                status.text = "Gen " + str(gen) + ", Best: " + str(creatures[0].score)
                #
                creatures[0].update(foods, ticks)
                #
                creatures[0].energy -= 1
                ticks += 1
                #
                for food in foods:
                    if checkCollision(creatures[0].rect, food.rect):
                        food.tbd = True
                        creatures[0].energy += FOOD_ENERGY
                #
                #if(ticks == int(TIME_CAP / 2)):
                #    for food in foods:
                #        food.rect.x  = (food.rect.x / 2) + WIDTH / 2
                #
                objects = list(filter(lambda obj: not obj.tbd, objects))
                foods = list(filter(lambda obj: not obj.tbd, foods))
                #
                if(creatures[0].energy < 0 or ticks > TIME_CAP or 
                creatures[0].rect.x < 0 or 
                creatures[0].rect.x > WIDTH or
                creatures[0].rect.y < 0 or
                creatures[0].rect.y > HEIGHT):
                    mode = 4
                #
                draw_window(objects)
            case 4:
                gen += 1
                species.append([])
                #
                partition = int(len(creatures) / 2)
                for x in range(partition):
                    new_data = creatures[x].brain.mutate()
                    sight = creatures[x].sight
                    sight += int(np.round(random.uniform(-1, 1)))
                    if sight < 1:
                        sight = 1
                    elif sight > 10:
                        sight = 10
                    creatures[x + partition] = Creature(WIDTH / 2, HEIGHT / 2, DUDEW, DUDEH, GREEN, creatures[x].id + CREATURE_NUM, new_data[0], new_data[1], sight)#create new,mutated creature
                #
                creatures[CREATURE_NUM - 1] = Creature(WIDTH / 2, HEIGHT / 2, DUDEW, DUDEH, GREEN, cr_id)
                cr_id += 1
                #
                for cr in creatures:
                    cr.reset()
                #
                objects = [status]
                #
                cr_num = 0
                sum = 0
                mode = 0
    #
    xns = []
    for x in range(len(bests)):
        xns.append(x)
    xs = np.array(xns)
    ys = np.array(bests)
    ays = np.array(avgs)
    #
    spc_num = np.zeros((CREATURE_NUM, len(species)))
    for gen in range(len(species)):
        for sp in species[gen]:
            spc_num[sp][gen] += 1
    #
    spc_np = np.vstack(spc_num)
    #
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Creatures over time')
    #
    ax1.plot(xs, ys)
    ax1.plot(xs, ays)
    plt.ylim([0, high_cr])
    #
    ax2.stackplot(xs, spc_np)
    #
    plt.show()
    #
    pygame.quit()

main()

#c1 = Creature(20, 20, 20, 20, WHITE, 0)
#print(c1.brain)
#new_data = c1.brain.mutate()
#c2 = Creature(20, 20, 20, 20, WHITE, 0, new_data[0], new_data[1], 5)
#print(c2.brain)