import os
import random

path = os.getcwd()
print(path)
class Doodler():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r_img = loadImage(path + "/assets/" + "lik-right.png")
        self.l_img = loadImage(path + "/assets/" + "lik-left.png")
        self.img_w = w
        self.img_h = h
        self.dir = RIGHT
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.accel_g = 0.8
        self.climb = 0
    
    def display(self):
        self.update()
        if self.dir is RIGHT:
            image(self.r_img, self.x, self.y)
        else:
            image(self.l_img, self.x, self.y)
        
    def update(self): # from example project
        if self.y > height+25:
            game.gameOver()
            
        if self.key_handler[LEFT] == True:
            self.x += -6
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.x += 6
            self.dir = RIGHT
        self.vy += self.accel_g
        for platform in game.platforms:
            if (((self.y >= platform.y-50) and (self.y <= platform.y) and (self.vy >= 0)) and ((self.x >= platform.x-25) and (self.x <= platform.x+platform.w))):
                self.y = platform.y-70
                self.vy = -15
                if game.score/100 > 200:
                    if random.randint(0, 5) > 3:
                        platform.destroy()
                elif game.score/100 > 500:
                    platform.destroy()
        self.x += self.vx
        self.y += self.vy
        
        if self.x <= 0:
            self.x = (width+self.x)
        if self.x >= width:
            self.x = (self.x-width)
            
        if self.y < game.h//2:
            self.climb = (game.h//2-self.y)
            self.y = game.h//2
            for platform in game.platforms:
                platform.y += self.climb
                game.score += self.climb

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
        elif platformType == "fake":
            self.img = loadImage(path + "/assets/brown/brown_1.png")
            
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)
    
    def destroy(self):
        del self

class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.y_shift = 0
        self.platforms = []
        self.backgroundImage = loadImage(path+"/assets/bck@2x.png")
        self.addPlatforms(8)
        self.doodler = Doodler(self.platforms[0].x, self.platforms[0].y - 100, 35, 50)
        self.score = 0
        self.isStarted = True
        self.level = 0
    
    def addPlatforms(self, n):
        for i in range(n-1, -1, -1):
            x = random.randint(0, self.w-80)
            y = (self.h//8)*i
            self.platforms.append(Platform(x, y, 80, 20, "stable"))
        
    def display(self):
        if self.isStarted:
            strokeWeight(0)
            image(self.backgroundImage,0,0)
            # self.checkPlatforms()
            for platform in self.platforms:
                platform.display()
            self.doodler.display()
            platform_manager()
            fill(0, 0, 0)
            textSize(30)
            text("Score: "+str(game.score//100), 20, 40)
            if self.score//100 >= 1000:
                self.level = 2
            elif self.score//100 >= 500:
                self.level = 1
            else:
                self.level = 0
        else:
            background(0)
            fill(255, 255, 255)
            textAlign(CENTER, CENTER)
            textSize(80)
            text("GAME", width/2, 2*height/10)
            text("OVER", width/2, 3*height/10)
            textSize(40)
            text("Score: "+str(game.score//100), width/2, 5*height/10)
            text("Retry: [CLICK]", width/2, 7*height/10)
            text("Exit: [ESC]", width/2, 8*height/10)
            textAlign(LEFT)
    
    def gameOver(self):
        self.isStarted = not self.isStarted

game = Game(400, 700)

def platform_manager():
    for p in game.platforms:
        if p.y > game.h:
            game.platforms.remove(p)
            
    while len(game.platforms) < 7:
        x = random.randint(0, game.w-80)
        y = abs(600-(120*len(game.platforms)))
        random_num = random.randint(0, 30) 
        if random_num > 25:
            new = Platform(x, y, 80, 20, "moving")
            game.platforms.append(new)
        elif random_num > 20:
            new = Platform(x, y, 80, 20, "fake")
            game.platforms.append(new)
        else:    
            new = Platform(x, y, 80, 20, "stable")
            game.platforms.append(new)

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
    elif keyCode == ESC:
        pass
    
def keyReleased():
    if keyCode == LEFT:
        game.doodler.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.doodler.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.doodler.key_handler[UP] = False

def mousePressed():
    if not game.isStarted:
        game.isStarted = True
        game.score = 0
        game.platforms = []
        game.addPlatforms(8)
        game.doodler.x = game.platforms[0].x
        game.doodler.y = game.platforms[0].y - 100
