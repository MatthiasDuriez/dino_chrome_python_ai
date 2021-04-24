import pygame
import neat
import time
import os
import random
pygame.font.init()



DINO_IMG = [pygame.image.load(os.path.join("images/dino",'dino_3.png')),pygame.image.load(os.path.join("images/dino",'dino_4.png')),pygame.image.load(os.path.join("images/dino",'dino_7.png')),pygame.image.load(os.path.join("images/dino",'dino_8.png'))]
CACTUS_IMG = [pygame.image.load(os.path.join("images/cacti","cacti_large_1.png"))]
PTERA_IMG = [pygame.image.load(os.path.join("images/ptera","ptera_1.png"))]
GROUND_IMG = pygame.image.load(os.path.join("images","ground.png"))
BG_IMAGE = pygame.image.load(os.path.join("images","cloud.png"))

WIN_HEIGHT = 700
WIN_WIDTH = 1500

STAT_FONT = pygame.font.SysFont("comicsans",50)

class Dino:
    RUN_SPEED = 5
    VEL = 12
    def __init__(self, x):
        self.x = x
        self.y = WIN_HEIGHT-70-DINO_IMG[0].get_height()
        self.base = self.y
        self.img = DINO_IMG[0]
        self.img_count = 0
        self.img_index = 0
        self.tick_count = 0
        self.vel = self.VEL
        self.jumped = False
        self.height = self.y
        self.squating= False
        self.jumping = False
    
    def jump(self):
        self.vel = self.VEL
        self.tick_count = 0
        self.height = self.y
        self.jumped= True
    
    def squat(self):
        self.vel = self.VEL
        self.squating = True


    def input_handler(self, userInput):
        if userInput[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.squating = False
        if userInput[pygame.K_DOWN] and not self.jumping:
            self.squating = True
            self.jumping = False
        if not(userInput[pygame.K_DOWN] and self.squating):
            #self.jumping = False
            self.squating = False
        if self.jumping and not self.jumped:
            self.jump()
        if self.squating:
            self.squat()
        

    def move(self):
        if self.jumped==True:
            self.y -= self.vel*2
            self.vel -= 0.6
            if self.y >= self.base:
                self.jumped=False
                self.vel = self.VEL
                self.y = self.base
                self.jumping = False
            # self.tick_count += 1
            # d = self.vel*self.tick_count + 1.5*self.tick_count**1.9
            # if d >= 50:
            #     d = 50
            # if d < 0:
            #     d -= 1
            # self.y = self.y +d
            # if self.y >= self.base:
            #     self.y = self.base
            #     self.jumped=False
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self,win):
        self.img_count +=1
        self.img_index = 0
        if (self.squating):
            self.img_index = 2
        if not(self.jumping):
            self.y = WIN_HEIGHT-70-DINO_IMG[self.img_index].get_height()
        if self.img_count < self.RUN_SPEED:
            self.img = DINO_IMG[self.img_index]
        elif self.img_count < self.RUN_SPEED*2:
            self.img = DINO_IMG[self.img_index+1]
        elif self.img_count < self.RUN_SPEED*2+1:
            self.img = DINO_IMG[self.img_index]
            self.img_count=0
        win.blit(self.img, (self.x,self.y))

class Obstacle:
    IMG = CACTUS_IMG+PTERA_IMG
    def __init__(self,x,typeObstacle):
        self.x = x
        self.type = typeObstacle
        self.img = self.IMG[typeObstacle]
        self.vel = 7
        self.passed = False;
        if self.type == 0:
            self.y = WIN_HEIGHT-90-self.img.get_height()
        else:
            self.y = WIN_HEIGHT-100-self.img.get_height()-50

    def move(self,game_speed):
        self.vel = game_speed
        self.x -= self.vel
    def collide(self,dino):
        dino_mask = dino.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)
        offset = (self.x - dino.x, self.y - round(dino.y))
        collide_point = dino_mask.overlap(obstacle_mask,offset)
        if collide_point:
            return True
        return False

        
    def draw(self,win):
        win.blit(self.img, (self.x, self.y))

class Ground:
    
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self,y):
        self.vel = 7
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self,game_speed):
        self.vel = game_speed
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.WIDTH <0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH <0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def obstacle_gen(obstacles):
    if len(obstacles) == 3:
        return obstacles
    if len(obstacles) == 2:
        if(obstacles[1].x>WIN_WIDTH-400):
            return obstacles
        if(random.randrange(0,100)<=10):
           obstacles.append(Obstacle(WIN_WIDTH+10,random.randrange(0,2))) 
    if len(obstacles) == 1:
        if(obstacles[0].x>WIN_WIDTH-700):
            return obstacles
        obstacles.append(Obstacle(WIN_WIDTH+10,random.randrange(0,2))) 
    if len(obstacles) == 0:
        obstacles.append(Obstacle(WIN_WIDTH+10,random.randrange(0,2)))
    return obstacles
def obstacle_delete(obstacles):
    rem = []
    if len(obstacles)>0:
        for obstacle in obstacles:
            if obstacle.x+obstacle.img.get_width() < 0:
                rem.append(obstacle)
    if len(rem)>0:
        for obstacle in rem:
            obstacles.remove(obstacle)
    return obstacles

def draw_window(win,dino,ground,obstacles,score,game_speed):
    win.fill([255,255,255])
    if len(obstacles)>0:
        for obstacle in obstacles:
            obstacle.draw(win)
    text = STAT_FONT.render("Score "+ str(score),1 , (0,0,0))
    win.blit(text,(10,10))
    text = STAT_FONT.render("Speed "+ str(game_speed),1 , (0,0,0))
    win.blit(text,(10,50))
    ground.draw(win)
    dino.draw(win)
    pygame.display.update()

def main():
    clock_tick_count = 0
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    win.fill([255,255,255])
    clock = pygame.time.Clock()
    ground = Ground(WIN_HEIGHT-100)
    died = False
    run = True
    dino = Dino(20)
    obstacles = [Obstacle(WIN_WIDTH+10,0)]
    score = 0
    game_speed = 7
    
    while run:
        clock.tick(60)
        clock_tick_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            dino.input_handler(pygame.key.get_pressed())
        if died == False:
            score+=1
            if (score%200==0):
                game_speed+=1
            if len(obstacles)>0:
                for obstacle in obstacles:
                    if obstacle.collide(dino):
                        died=True
                    obstacle.move(game_speed)
            obstacles = obstacle_delete(obstacles)
            if clock_tick_count==60:
                obstacles = obstacle_gen(obstacles)
                clock_tick_count=0
            dino.move()
            ground.move(game_speed)
        draw_window(win,dino,ground,obstacles,score,game_speed)
main()