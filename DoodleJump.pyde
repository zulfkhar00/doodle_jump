import os
import random

path = os.getcwd()

class Creature:
    def __init__(self, x, y, r, g, img, w, h):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/assets/" + img)
        self.img_w = w
        self.img_h = h
        self.dir = RIGHT
        
    def gravity(self):
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy = self.vy + 0.65
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)

    def update(self):
        self.gravity()
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    
    def display(self):
        self.update()
        circle(self.x+self.r/2, self.y+self.r/2, self.r)
        image(self.img, self.x, self.y)

class Doodler():
    def __init__(self, x, y, r, g, img, w, h):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/assets/" + img)
        self.img_w = w
        self.img_h = h
        self.dir = RIGHT
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
    
    def display(self):
        self.update()
        rect(self.x, self.y, self.img_w, self.img_h)
        # circle(self.x+self.r/2, self.y+self.r/2, self.r)
        image(self.img, self.x, self.y)
    
    def update(self):
        self.gravity()
        if self.key_handler[LEFT] == True:
            self.vx = -8
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 8
            self.dir = RIGHT
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True and self.y + self.r == self.g:
            self.vy = -15

        self.x = self.x + self.vx
        self.y = self.y + self.vy
        
        if self.y < game.h//2:
            game.y_shift = game.h//2 - self.y
            self.y = game.h//2
            
            for p in game.platforms:
                p.y += game.y_shift
    
    def gravity(self):
        if self.y + 45 >= self.g:
            self.vy = -15
        else:
            self.vy = self.vy + 0.65
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        for i in range(len(game.platforms)):
            p = game.platforms[i]
            if self.y + self.img_h <= p.y and self.x-10 >= p.x and self.x+self.img_w+5 <= p.x + p.w:
                self.g = p.y
                fill(0, 125, 0)
                rect(p.x, p.y, p.w, p.h)
                break     
            else:
                self.g = game.g

class Platform:
    def __init__(self, x, y, w, h, platformType):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = platformType
        if platformType == "stable":
            self.img = loadImage(path + "/assets/platform1.png")
        elif platformType == "moving":
            self.img = loadImage(path + "/assets/platform2.png")
            
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)

class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.y_shift = 0
        self.doodler = Doodler(200, 350, 45, self.g, "lik-right.png", 35, 50)
        self.platforms = []
        self.backgroundImage = loadImage(path+"/assets/bck@2x.png")
        self.addPlatforms(8)
    
    def addPlatforms(self, n):
        for i in range(n):
            x = random.randint(0, self.w-80)
            y = (self.h//8)*i
            # y = random.randint(i*(self.h//8), (self.h//8)*(i+1))
            self.platforms.append(Platform(x, y, 80, 20, "stable"))
    
    def checkPlatforms(self):
        offScreenPlatforms = []
        for platform in game.platforms:
            if platform.y > game.h:
                offScreenPlatforms.append(platform)

        for p in offScreenPlatforms:
            game.platforms.remove(p)
            game.addPlatforms(1)
        
        
    def display(self):
        strokeWeight(0)
        image(self.backgroundImage,0,0)
        self.checkPlatforms()
        for platform in self.platforms:
            platform.display()
        self.doodler.display()

game = Game(400, 700, 700-30)

def setup():
    size(game.w, game.h)
    background(255, 255, 255)
    
def draw():
    background(255, 255, 255)
    game.display()
    
    

def keyPressed():
    if keyCode == LEFT:
        game.doodler.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.doodler.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.doodler.key_handler[UP] = True
    
def keyReleased():
    if keyCode == LEFT:
        game.doodler.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.doodler.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.doodler.key_handler[UP] = False
    
