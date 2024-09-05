import pygame
import sys
import random

print("Select difficulty:")
print("(slow, medium, fast)\n")
difficulty = input().lower()

speed = 0

if difficulty == "slow":
    speed = 5
elif difficulty == "fast":
    speed = 20
else:
    speed = 12

pygame.init()


SW, SH = 600, 600
BLOCK_SIZE = 40
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE * 2)


pygame.display.set_caption("Worm")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))

class Worm:
    #make worm
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False


    def update(self):
        global apple

        #check if dead
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True

        #reset if dead
        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            apple = Apple()

        #grow body
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)


class Apple:
    #make apple
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, "orange", self.rect)



#print score
score = FONT.render("1", True, "white")
score_rect = score.get_rect(center=(SW / 2, SH / 10))


#worm
worm = Worm()

#apple
apple = Apple()



while True:
    for event in pygame.event.get():
        #exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                worm.ydir = 1
                worm.xdir = 0
            elif event.key == pygame.K_UP:
                worm.ydir = -1
                worm.xdir = 0
            elif event.key == pygame.K_RIGHT:
                worm.ydir = 0
                worm.xdir = 1
            elif event.key == pygame.K_LEFT:
                worm.ydir = 0
                worm.xdir = -1

    screen.fill('black')
    worm.update()

    apple.update()

    score = FONT.render(f"{len(worm.body) + 1}", True, "white")

    pygame.draw.rect(screen, "pink", worm.head)

    for square in worm.body:
        pygame.draw.rect(screen, "pink", square)

    screen.blit(score, score_rect)

    #eat
    if worm.head.x == apple.x and worm.head.y == apple.y:
        worm.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()

    pygame.display.update()
    clock.tick(speed)




