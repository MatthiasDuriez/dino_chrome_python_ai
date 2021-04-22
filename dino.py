import pygame
import neat
import time
import os
import random
pygame.font.init()



DINO_IMG = [pygame.image.load(os.path.join("images/dino",'dino_3.png')),pygame.image.load(os.path.join("images/dino",'dino_4.png'))]
CACTUS_IMG = [pygame.image.load(os.path.join("images/cacti","cacti_large_1.png"))]
PTERA_IMG = [pygame.image.load(os.path.join("images/ptera","ptera_1.png"))]
GROUND_IMG = pygame.image.load(os.path.join("images","ground.png"))
BG_IMAGE = pygame.image.load(os.path.join("images","cloud.png"))

WIN_HEIGHT = 700
WIN_WIDTH = 1500

STAT_FONT = pygame.font.SysFont("comicsans",50)

class Dino:
    RUN_SPEED = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base = y
        self.img = DINO_IMG[0]
        self.img_count = 0
        self.tick_count = 0
        self.vel = 0
        self.jumped = False
        self.height = self.y
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        self.jumped= True

    def move(self):
        if self.jumped==True:
            self.tick_count += 1
            d = self.vel*self.tick_count + 1.5*self.tick_count**2
            if d >= 16:
                d = 16
            if d < 0:
                d -= 2
            self.y = self.y +d
            if self.y >= self.base:
                self.y = self.base
                self.jumped=False
        

    def draw(self,win):
        self.img_count +=1
        if self.img_count < self.RUN_SPEED:
            self.img = DINO_IMG[0]
        elif self.img_count < self.RUN_SPEED*2:
            self.img = DINO_IMG[1]
        elif self.img_count < self.RUN_SPEED*2+1:
            self.img = DINO_IMG[0]
            self.img_count=0
        win.blit(self.img, (self.x,self.y))

class Obstacle:
    IMG = CACTUS_IMG+PTERA_IMG
    VEL = 7
    def __init__(self,x,typeObstacle):
        self.x = x
        self.type = typeObstacle
        self.img = self.IMG[typeObstacle]
        self.vel = self.VEL
        if self.type == 0:
            self.y = WIN_HEIGHT-100-self.img.get_height()
        else:
            self.y = WIN_HEIGHT-100-self.img.get_height()

    def move(self):
        self.x -= self.VEL
        
    def draw(self,win):
        win.blit(self.img, (self.x, self.y))

class Ground:
    VEL = 7
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH <0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH <0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def obstacle_gen(obstacles):
    if len(obstacles) > 3:
        return obstacles
    if len(obstacles) == 0:
        return obstacles

def draw_window(win,dino,ground,obstacles):
    win.fill([255,255,255])
    for obstacle in obstacles:
            obstacle.draw(win)
    ground.draw(win)
    dino.draw(win)
    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    win.fill([255,255,255])
    clock = pygame.time.Clock()
    ground = Ground(WIN_HEIGHT-100)
    run = True
    dino = Dino(20,WIN_HEIGHT-100-70)
    obstacles =[Obstacle(700,0)]
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dino.jump()
        for obstacle in obstacles:
            obstacle.move()
        dino.move()
        ground.move()
        draw_window(win,dino,ground,obstacles)
main()