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
        self.accel_g = 1
        self.climb = 0
    
    def display(self):
        self.update()
        rect(self.x, self.y, self.img_w, self.img_h)
        image(self.img, self.x, self.y)
        
    def update(self): # from example project
        if self.key_handler[LEFT] == True:
            self.x += -6
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.x += 6
            self.dir = RIGHT
        self.vy += self.accel_g
        for platform in game.platforms:
            if (((self.y >= platform.y-50) and (self.y <= platform.y) and (self.vy >= 0)) and ((self.x >= platform.x-25) and (self.x <= platform.x+platform.w))):
                self.y = platform.y-25
                self.vy = -20
                #print(self.score/100)
                if game.score/100 > 200:
                    if random.randint(5) > 3:
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
            
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)
    
    def destroy(self):
        self.x = 600

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
        self.score = 0
    
    def addPlatforms(self, n):
        for i in range(n-1, -1, -1):
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
            game.addPlatforms(1) # todo 
        
        
    def display(self):
        strokeWeight(0)
        image(self.backgroundImage,0,0)
        # self.checkPlatforms()
        for platform in self.platforms:
            platform.display()
        self.doodler.display()
        platform_manager()

game = Game(400, 700, 700-30)

def platform_manager():
    #checks if platforms have fallen off the bottom of the screen and deletes them
    for p in game.platforms:
        if p.y > game.h:
            game.platforms.remove(p)
        else:
            pass
    #makes sure that there are always 6 platforms on the screen
    while len(game.platforms) < 6:
        x = random.randint(0, game.w-80)
        y = 600-(120*len(game.platforms))
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
    elif keyCode == UP:
        game.doodler.key_handler[UP] = True
    
def keyReleased():
    if keyCode == LEFT:
        game.doodler.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.doodler.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.doodler.key_handler[UP] = False
    
