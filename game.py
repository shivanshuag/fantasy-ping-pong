import pygame, sys
import random
import math
from pygame.locals import *
import pygame.mixer
import Tkinter
import tkSimpleDialog
import os

pygame.init()
bif = "bg1.jpg"
number_of_particles = 1
background_colour = (255, 255, 255)
(width, height) = (640, 360)
myfont = pygame.font.SysFont("comicsansms", 72)

screen = pygame.display.set_mode((640, 360), 0, 32)
background = pygame.image.load(bif).convert()
mif = "bar.png"
kif = "bigbar.png"
heart = "life.png"
over = "GameOver.png"
bulletpowerimg = "bulletpower.jpg"
bulletimg = "bullet.png"
extendbarimg = "barpower.png"
bar = pygame.image.load(mif).convert_alpha()
lifeimg = pygame.image.load(heart).convert_alpha()
gameover = pygame.image.load(over).convert_alpha()
bulletpower = pygame.image.load(bulletpowerimg).convert_alpha()
bullet = pygame.image.load(bulletimg).convert_alpha()
extendbar = pygame.image.load(kif).convert_alpha()
#sound = pygame.mixer.Sound(paddleball)
extendbarpower = pygame.image.load(extendbarimg).convert_alpha()
bulletwidth = 37
bulletheight = 12
bar_height = 44
bigbar_height = 87
flag = 0
sound = pygame.mixer.Sound("collision.wav")
gunshot = pygame.mixer.Sound("gunshot.wav")


class Player():
    def __init__(self,number,(x,y)):
        self.lives = 5
        self.number = number
        self.x = x
        self.y = y
        self.bar_height = 44
        self.bullet_display = 0
        self.bar_display = 0
        self.bullet_power = 0
        self.bar_power = 0
        self.bullets = 5
        if self.number == 1:
            self.bulletx = [0,0,0,0,0]
        else:
            self.bulletx = [640,640,640,640,640]
        self.bullety = [0,0,0,0,0]
    def loselife(self):
        self.lives -= 1
        self.bullet_power = 0
        self.bar_power = 0
        player1.y = 180
        player2.y = 180
        pygame.time.delay(500)
    def fire(self):
        if self.bullets>0:
            self.bullets-=1
            if(self.number == 1):
                self.bulletx[self.bullets] = 20
                self.bullety[self.bullets] = self.y
                
            else:
                self.bulletx[self.bullets] = 639
                self.bullety[self.bullets] = self.y
    def bullet(self):
        for num_bullet in range(0,5):        
            if(self.bulletx[num_bullet]>0 and self.bulletx[num_bullet]<640):
                    screen.blit(bullet,(self.bulletx[num_bullet],self.bullety[num_bullet]))
                    if(self.number == 1):          
                        self.bulletx[num_bullet] = self.bulletx[num_bullet]+0.1
                    else:
                        self.bulletx[num_bullet] = self.bulletx[num_bullet]-0.1
            if(player1.bulletx[num_bullet]>640):
                player1.bulletx[num_bullet] = 0
    def power(self,power_type):
        if power_type == "bullet":
            self.bullet_display = 1
        elif power_type == "extendbar":
            self.bar_display = 1
            
    def powergained(self,half_x,power_type,power_height):
        if (half_x < 7 or half_x > 633) and self.y < 180 + power_height and self.y > 180 - self.bar_height:
            if power_type == "bullet":
                self.bullet_power = 1
                self.bullets = 5
            if power_type == "barextend":
                self.bar_power = 1

    def bulletcheck(self, player):
        for num_bullet in range(0, 5):        
                if self.bulletx[num_bullet]> 633 - bulletwidth and self.number == 1 and self.bullety[num_bullet] > player.y - bulletheight and self.bullety[num_bullet] < player.y + player.bar_height:
                    player.loselife()
                    self.bulletx[num_bullet] = 0
                elif ((self.bulletx[num_bullet] < 7 and self.bulletx[num_bullet] >0) and (self.number == 2) and (self.bullety[num_bullet] > player.y - bulletheight) and (self.bullety[num_bullet] < player.y + player.bar_height)):
                    player.loselife()
                    print self.bullety[num_bullet]
                    print player.y - bulletheight
                    self.bulletx[num_bullet] = 640
            
                    
class Particle():
    def __init__(self, (x, y), size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (255, 255, 255)
        self.thickness = 0
        self.speedx = 0
        self.speedy = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self,player1,player2):
        if self.x > width - self.size - 7 and self.y > player2.y - self.size and self.y < player2.y + self.size + player2.bar_height   :
            self.angle = - self.angle
            sound.play()

        elif self.x > width - self.size:
            player2.loselife()
            self.x = 320
            self.y = 180
            flag = 1
            
        elif self.x <  self.size + 7 and self.y > player1.y - self.size and self.y < player1.y + self.size + player1.bar_height:
            self.angle = - self.angle
            sound.play()
            
        elif self.x < self.size:
            player1.loselife()
            flag = 1 
            self.x = 320
            self.y = 180
            

        if self.y > height - self.size:
            self.angle = math.pi - self.angle

        elif self.y <  self.size:
            self.angle = math.pi - self.angle

def restart(player1, player2):
    python = sys.executable
    os.execl(python, python, * sys.argv)
root = Tkinter.Tk()
root.withdraw()
num_balls = tkSimpleDialog.askinteger("Balls","No. of balls?")
if(num_balls == None):
    num_balls = 1
#print num_balls    
set_speed = tkSimpleDialog.askinteger("Speed","Set the speed of the balls")
if(set_speed == None):
    set_speed = 1
player1_name = tkSimpleDialog.askstring("Name","Name of player 1")
player2_name = tkSimpleDialog.askstring("Name","Name of player 2")
label1 = myfont.render(player1_name+" wins!", 1, (0, 128, 0))
label2 = myfont.render(player2_name+" wins!", 1, (0, 128, 0))
pygame.display.set_caption('Ping Pong')
halfx_1 = 320
halfx_2 = 320

number_of_particles = num_balls
#print number_of_particles
my_particles = []
x2,y2 = 633,180
x1,y1 = 0,180
power_counter = 0
bar_counter1 = 0
bar_counter2 = 0
player1 = Player(1,(x1,y1))
player2 = Player(2,(x2,y2))
for n in range(number_of_particles):
    size = 8
    x = 320
    y = 180
    particle = Particle((x, y), size)
#particle.speedx = 5
#particle.speedy = 5
    particle.speed = math.log(set_speed+1,30)/3
    particle.angle = random.uniform(-math.pi/3 ,math.pi/3)
    if n == 0 :
        particle.angle = random.uniform(math.pi/4, math.pi/6)
    if n == 1:
        particle.angle = random.uniform(-math.pi/6, -math.pi/4)  

    my_particles.append(particle)
powercounter = 1
running = True
counter = 0
movey2 = 0
movey1 = 0
while running:

    #print player1.lives
    counter = counter + 1
    if player1.lives == 0:
        screen.blit(gameover, (0, 0))
        screen.blit(label2, (180, 230))
    if player2.lives == 0:
        screen.blit(gameover, (0, 0))
        screen.blit(label1, (180, 230))      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and player1.bullet_power == 1:
            player1.fire()
            gunshot.play()
        if event.type == pygame.KEYUP and event.key == pygame.K_RCTRL and player2.bullet_power == 1:
            player2.fire()
            gunshot.play()
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        movey2 = -0.1
    elif keys[K_DOWN]:
        movey2 = +0.1
    elif keys[K_w]:
        movey1 = -0.1
    elif keys[K_s]:
        movey1 = +0.1
    elif keys[K_F5]:
        restart(player1, player2)
        player1 = Player(1,(0,180))
        player2 = Player(2,(633,180))
        continue
    if(player2.y<0 and movey2<0):
        1   
    elif(player2.y>336 and movey2>0):
        1    
    else:
        player2.y+=movey2
        y2 = player2.y

    if(player1.y<0 and movey1<0):
        1   
    elif(player1.y>336 and movey1>0):
        1    
    else:
        player1.y+=movey1
        y1 = player1.y
    movey2 = 0
    movey1 = 0
    
    if player1.bar_power == 1:
        bar_counter1 = bar_counter1 + 1
        if bar_counter1 == 20000:
            bar_counter1 = 0
            player1.bar_power = 0
    if player2.bar_power == 1:
        bar_counter2 = bar_counter2 + 1
        if bar_counter2 == 20000:
            bar_counter2 = 0
            player2.bar_power = 0
    #screen.fill(background_colour)
    if player1.lives>0 and player2.lives>0:
        #print player2.lives
        screen.blit(background,(0,0))
        #screen.blit(label, (200, 100))

        if player1.bar_power == 0:
            screen.blit(bar,(player1.x,player1.y))
            player1.bar_height = 44
        else:
            screen.blit(extendbar,(player1.x,player1.y))
            player1.bar_height = 87

        if player2.bar_power == 0:
            screen.blit(bar,(player2.x,player2.y))
            player2.bar_height = 44
        else:
            screen.blit(extendbar,(player2.x,player2.y))
            player2.bar_height = 87
        
        for life in range(0,player1.lives):
            screen.blit(lifeimg,(30*life,10))
        for life in range(0,player2.lives):
            screen.blit(lifeimg,(640-30*(life+1),10))
        for particle in my_particles:
            particle.move()
            particle.bounce(player1,player2)
            particle.display()
            player1.bullet()
            player2.bullet()
            player1.bulletcheck(player2)
            player2.bulletcheck(player1)
#           print pygame.time.get_ticks()
            powercounter = powercounter + 1
            print powercounter
        if powercounter%20000 == 0:
            power_counter = power_counter + 1
            powercounter = 0           
 #           print "20 sec ho gaye"
            if power_counter % 2 == 0:
                player1.power("bullet")
                player2.power("bullet")
                power_counter = 0
                print player1.bar_display
            else:
                player1.power("extendbar")
                player2.power("extendbar")
                print player1.bar_display
        if player1.bullet_display == 1:   
            screen.blit(bulletpower, (halfx_1, 180))
            player1.powergained(halfx_1, "bullet", 47)
            halfx_1 = halfx_1 - 0.1
            if halfx_1 < 0:
                player1.bullet_display = 0
                halfx_1 = 320
        if player2.bullet_display == 1:   
            screen.blit(bulletpower, (halfx_2, 180))
            player2.powergained(halfx_2, "bullet", 47)
            halfx_2 = halfx_2 + 0.1
            if halfx_2 > 640:
                player2.bullet_display = 0
                halfx_2 = 320
        if player1.bar_display == 1:   
            screen.blit(extendbarpower, (halfx_1, 180))
            player1.powergained(halfx_1, "barextend", 50)
            halfx_1 = halfx_1 - 0.1
            if halfx_1 < 0:
                player1.bar_display = 0
                print "0 ho gayi"
                halfx_1 = 320
        if player2.bar_display == 1:   
            screen.blit(extendbarpower, (halfx_2, 180))
            player2.powergained(halfx_2, "barextend", 50)
            halfx_2 = halfx_2 + 0.1
            if halfx_2 > 640:
                player2.bar_display = 0
                halfx_2 = 320
    
            
    pygame.display.update()
