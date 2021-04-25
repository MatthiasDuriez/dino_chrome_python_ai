import pygame
import neat
import time
import os
import random

import visualize
pygame.font.init()



DINO_IMG = [pygame.image.load(os.path.join("images/dino",'dino_3.png')),pygame.image.load(os.path.join("images/dino",'dino_4.png')),pygame.image.load(os.path.join("images/dino",'dino_7.png')),pygame.image.load(os.path.join("images/dino",'dino_8.png'))]
CACTUS_IMG = [pygame.image.load(os.path.join("images/cacti","cacti_large_1.png"))]
PTERA_IMG = [pygame.image.load(os.path.join("images/ptera","ptera_1.png")),pygame.image.load(os.path.join("images/ptera","ptera_1.png")),pygame.image.load(os.path.join("images/ptera","ptera_1.png"))]
GROUND_IMG = pygame.image.load(os.path.join("images","ground.png"))
BG_IMAGE = pygame.image.load(os.path.join("images","cloud.png"))

WIN_HEIGHT = 700
WIN_WIDTH = 1500

GEN=0

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
        self.died = False
    
    def jump(self):
        self.vel = self.VEL
        self.tick_count = 0
        self.height = self.y
        self.jumped= True
    
    def squat(self):
        self.vel = self.VEL


    def input_handler(self, jump , squat):
        if jump>0.5 and not self.jumping:
            self.jumping = True
            self.squating = False
        if squat>0.5:
            self.squating = True
        if not(squat>0.5 and self.squating):
            #self.jumping = False
            self.squating = False
        if self.jumping and not self.jumped:
            self.jump()
            return -0.5
        if self.squating and not self.jumped:
            self.squat()
        return 0
        

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
        if not self.died:
            self.img_count +=1
            if (self.jumping or not self.squating):
                self.img_index = 0
            if (self.squating and not self.jumping):
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
        if self.died:
            self.img = DINO_IMG[4]
        win.blit(self.img, (self.x,self.y))

class Obstacle:
    VEL = 7 
    IMG = CACTUS_IMG+PTERA_IMG
    def __init__(self,x,typeObstacle):
        self.x = x
        self.type = typeObstacle
        self.img = self.IMG[typeObstacle]
        self.vel = self.VEL
        self.passed = False;
        if self.type == 0:
            self.y = WIN_HEIGHT-90-self.img.get_height()
        elif self.type == 1:
            self.y = WIN_HEIGHT-100-self.img.get_height()-50
        elif self.type == 2:
            self.y = WIN_HEIGHT-100-self.img.get_height()+20
        elif self.type == 3:
            self.y = WIN_HEIGHT-100-self.img.get_height()-170

    def move(self,game_speed):
        self.vel = self.VEL * game_speed
        self.x -= self.vel
    def collide(self,dino):
        dino_mask = dino.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)
        offset = (round(self.x) - dino.x, self.y - round(dino.y))
        collide_point = dino_mask.overlap(obstacle_mask,offset)
        if collide_point:
            return True
        return False

        
    def draw(self,win):
        win.blit(self.img, (self.x, self.y))

class Ground:
    
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG
    VEL = 7
    def __init__(self,y):
        self.vel = self.VEL
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self,game_speed):
        self.vel = self.VEL * game_speed
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
        if(random.randrange(0,100)<=30):
            if (random.randrange(0,3)<2):
                obstacles.append(Obstacle(random.randrange(WIN_WIDTH+300,WIN_WIDTH+600),0)) 
            else:
                obstacles.append(Obstacle(random.randrange(WIN_WIDTH+300,WIN_WIDTH+600),random.randrange(1,4)))
    if len(obstacles) == 1:
        if(obstacles[0].x>WIN_WIDTH-400):
            return obstacles
        if (random.randrange(0,3)<2):
                obstacles.append(Obstacle(random.randrange(WIN_WIDTH+300,WIN_WIDTH+600),0)) 
        else:
            obstacles.append(Obstacle(random.randrange(WIN_WIDTH+300,WIN_WIDTH+600),random.randrange(1,4))) 
    if len(obstacles) == 0:
        if (random.randrange(0,3)<2):
            obstacles.append(Obstacle(random.randrange(WIN_WIDTH+300,WIN_WIDTH+600),0)) 
        else:
            obstacles.append(Obstacle(random.randrange(WIN_WIDTH+300,WIN_WIDTH+600),random.randrange(1,4))) 
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

def draw_window(win,dinos,ground,obstacles,score,game_speed,gen,alive_nb):
    win.fill([255,255,255])
    if len(obstacles)>0:
        for obstacle in obstacles:
            obstacle.draw(win)
    text = STAT_FONT.render("Score "+ str(score),1 , (0,0,0))
    win.blit(text,(10,10))
    text = STAT_FONT.render("Gen "+ str(gen),1 , (0,0,0))
    win.blit(text,(10,50))
    text = STAT_FONT.render("Alive "+ str(alive_nb),1 , (0,0,0))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
    ground.draw(win)
    for x,dino in enumerate(dinos):
        dino.draw(win)
        if x == 10:
            break
    pygame.display.update()

def main(genomes,config):
    global GEN
    GEN +=1
    nets = []
    ge = []
    dinos = []
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(20))
        g.fitness = 0
        ge.append(g)
    clock_tick_count = 0
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    win.fill([255,255,255])
    clock = pygame.time.Clock()
    ground = Ground(WIN_HEIGHT-100)
    died = False
    run = True
    obstacles = [Obstacle(WIN_WIDTH+10,0)]
    score = 0
    game_speed = 1
    
    while run:
        clock.tick(120)
        clock_tick_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            #dino.input_handler(pygame.key.get_pressed())
        obstacle_ind = 0
        if len(dinos)>0:
            if len(obstacles)>1 and dinos[0].x > round(obstacles[0].x) + obstacles[0].img.get_width():
                obstacle_ind = 1
        else:
            run = False
            break
        rem = []
        score+=1
        if (score%20==0):
            game_speed+=0.01
        if len(obstacles)>0:
            for obstacle in obstacles:
                for x,dino in enumerate(dinos):
                    if obstacle.collide(dino):
                        ge[x].fitness -= 2
                        if obstacle.type == 3:
                            ge[x].fitness -=2
                        dinos.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                obstacle.move(game_speed)
        
        
        if clock_tick_count==60:
            obstacles = obstacle_gen(obstacles)
            clock_tick_count=0
        for x,dino in enumerate(dinos):
            ge[x].fitness+=0.05
            dino.move()
            if(len(obstacles)>0):
                output = nets[x].activate((dino.y, obstacles[obstacle_ind].y,game_speed,obstacles[obstacle_ind].x))
                ge[x].fitness+=dino.input_handler(output[0],output[1])
        obstacles = obstacle_delete(obstacles)
        ground.move(game_speed)
        #draw_window(win,dinos,ground,obstacles,score,game_speed,GEN,len(dinos))
    
def main_window(genomes,config):
    global GEN
    GEN +=1
    nets = []
    ge = []
    dinos = []
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(20))
        g.fitness = 0
        ge.append(g)
    clock_tick_count = 0
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    win.fill([255,255,255])
    clock = pygame.time.Clock()
    ground = Ground(WIN_HEIGHT-100)
    died = False
    run = True
    obstacles = [Obstacle(WIN_WIDTH+10,0)]
    score = 0
    game_speed = 1
    
    while run:
        clock.tick(120)
        clock_tick_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            #dino.input_handler(pygame.key.get_pressed())
        obstacle_ind = 0
        if len(dinos)>0:
            if len(obstacles)>1 and dinos[0].x > round(obstacles[0].x) + obstacles[0].img.get_width():
                obstacle_ind = 1
        else:
            run = False
            break
        rem = []
        score+=1
        if (score%20==0):
            game_speed+=0.01
        if len(obstacles)>0:
            for obstacle in obstacles:
                for x,dino in enumerate(dinos):
                    if obstacle.collide(dino):
                        ge[x].fitness -= 2
                        if obstacle.type == 3:
                            ge[x].fitness -=2
                        dinos.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                obstacle.move(game_speed)
        
        
        if clock_tick_count==60:
            obstacles = obstacle_gen(obstacles)
            clock_tick_count=0
        for x,dino in enumerate(dinos):
            ge[x].fitness+=0.05
            dino.move()
            if(len(obstacles)>0):
                output = nets[x].activate((dino.y, obstacles[obstacle_ind].y,game_speed,obstacles[obstacle_ind].x))
                ge[x].fitness+=dino.input_handler(output[0],output[1])
        obstacles = obstacle_delete(obstacles)
        ground.move(game_speed)
        draw_window(win,dinos,ground,obstacles,score,game_speed,GEN,len(dinos))

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    #This is running up to 50 generations
    winner = p.run(main,50)
    visualize.draw_net(config, winner,True)
    visualize.plot_stats(stats)
    visualize.plot_species(stats)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)