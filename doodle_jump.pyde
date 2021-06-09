import os
import random
import json

path = os.getcwd()

# In total the logic of the game is divided into Bullet, Doodler, Platform, Enemy, Booster, Game classes
class Bullet:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/assets/" + "spray.png")
    
    def display(self):
        self.update()
        image(self.img, self.x, self.y, self.w, self.h)
    def update(self):
        for e in game.enemies:
            if (self.x > e.x and self.x < e.x+e.w) and (self.y >= e.y and self.y <= e.y+e.h):
                game.enemies.remove(e)
        self.y = self.y - 10

class Doodler():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r_img = loadImage(path + "/assets/" + "lik-right.png")
        self.l_img = loadImage(path + "/assets/" + "lik-left.png")
        self.up_img = loadImage(path + "/assets/" + "lik-puca.png") 
        self.with_jetpack_l_img = loadImage(path + "/assets/" + "with_jetpack_l.png")
        self.with_jetpack_r_img = loadImage(path + "/assets/" + "with_jetpack_r.png")
        self.img_w = w
        self.img_h = h
        self.dir = RIGHT
        self.last_dir = RIGHT
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.accel_g = 0.8
        self.climb = 0
        self.bullets = []
        self.isBoosted = False
    
    def display(self): # this method shows all the images and animations of Doodler
        self.update()
        if self.vy < -35:
            if self.dir is RIGHT:
                image(self.with_jetpack_r_img, self.x, self.y, self.img_w+10, self.img_h)
            elif self.dir is LEFT:
                image(self.with_jetpack_l_img, self.x, self.y, self.img_w+30, self.img_h+20)
        else:
            if self.dir is RIGHT:
                image(self.r_img, self.x, self.y)
            elif self.dir is UP:
                image(self.up_img, self.x, self.y)
            else:
                image(self.l_img, self.x, self.y)
        
    def update(self): # this method deals with the logical component of the Doodler (i.e. physics and so on)
        if self.y > height+25:
            game.gameOver()
            
        if self.key_handler[LEFT] == True:
            self.x += -6
            self.dir = LEFT
            self.last_dir = LEFT 
        elif self.key_handler[RIGHT] == True:
            self.x += 6
            self.dir = RIGHT
            self.last_dir = RIGHT
        elif self.key_handler[UP] == True:
            if len(self.bullets) == 0:
                newBullet = Bullet(self.x+20, self.y, 20, 20)
                self.bullets.append(newBullet)
            elif self.bullets[-1].y < 200:
                newBullet = Bullet(self.x+20, self.y, 20, 20)
                self.bullets.append(newBullet)
            self.dir = UP
        else:
            self.dir = self.last_dir
        
        for bullet in self.bullets:
            if bullet.y <= 0:
                self.bullets.remove(bullet)
        for bullet in self.bullets:
            bullet.display()
        
        if not self.isBoosted:
            self.vy += self.accel_g
            for platform in game.platforms: # the logic of comparing the coordinates of the Doodler and the platforms
                if (((self.y+self.img_h >= platform.y) and (self.y+self.img_h <= platform.y+platform.h) and (self.vy >= 0)) and ((self.x >= platform.x-25) and (self.x <= platform.x+platform.w))):
                    self.y = platform.y-70
                    self.vy = -15
                    platform.isTouched = True
                    if game.level == 1:
                        platform.destroy()
        else:
            self.vy -= 100
        self.x += self.vx
        self.y += self.vy
        # the logic of illusion of teleportation from side to side
        if self.x <= 0:
            self.x = (width+self.x)
        if self.x >= width:
            self.x = (self.x-width)
        # the logic of shifting the screen downwards
        if self.y < game.h//2:
            self.climb = (game.h//2-self.y)
            self.y = game.h//2
            for platform in game.platforms:
                platform.y += self.climb
                game.score += self.climb
            for enemy in game.enemies:
                enemy.y += self.climb
            for booster in game.boosters:
                booster.y += self.climb

class Platform:
    def __init__(self, x, y, w, h, platformType):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 2
        self.delegate = None
        self.type = platformType
        self.isTouched = False
        if platformType == "stable":
            self.img = loadImage(path + "/assets/platform1.png")
        elif platformType == "moving":
            self.img = loadImage(path + "/assets/platform2.png")
        elif platformType == "fake":
            self.img = loadImage(path + "/assets/brown/brown_1.png")
            self.brown_img = []
            for i in range(1, 7):
                self.brown_img.append(loadImage(path + "/assets/brown/brown_"+str(i)+".png"))
            
    def display(self):
        self.blueMove()
        if self.type == 'fake':
            if self.isTouched:
                for i in range(5):
                    image(self.brown_img[i], self.x, self.y, self.w, self.h)
                for p in game.platforms[::-1]:
                    if p.type == 'fake' and p.isTouched and game.doodler.vy > 0:
                        # self.sound_brown.rewind()
                        # self.sound_brown.play()
                        game.platforms.remove(p)
                        break
            else:
                image(self.brown_img[0], self.x, self.y, self.w, self.h)
        else:
            image(self.img, self.x, self.y, self.w, self.h)
    
    def destroy(self):
        del self
        
    def blueMove(self): # this method moves the blue platforms
        if self.type == "moving":
            if self.x + self.w >= game.w - 5:
                self.vx = -2
            elif self.x <= 5:
                self.vx = 2
            self.x += self.vx
            if self.delegate is not None:
                self.delegate.x = self.x

class Enemy:
    def __init__(self, x, y, w, h, enemyType):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = enemyType
        self.vx = 2
        self.vy = 2
        self.img = loadImage(path + "/assets/" + enemyType + ".png")
    def update(self):
        d = game.doodler
        if d.vy < -35:
            pass
        else:
            if (self.x > d.x and self.x < d.x+d.img_w) and (self.y >= d.y and self.y <= d.y+d.img_h):
                game.gameOver()
    def display(self):
        self.update()
        image(self.img, self.x, self.y, self.w, self.h)

class Booster:
    def __init__(self, x, y, w, h, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
        self.img = loadImage(path + "/assets/" + "jetpack1" + ".png")
        self.time = 0
        
    def update(self):
        d = game.doodler
        if (d.x+d.img_w > self.x and d.x < self.x+self.w) and (self.y >= d.y and self.y <= d.y+d.img_h):
            game.doodler.isBoosted = True
            self.jetpack()
        else:
            game.doodler.isBoosted = False
    
    def jetpack(self): # the logic of interaction of Doodler and Jetpack Booster
        if self.time < 100:
            self.time += 1
            game.doodler.vy = 0
        else:
            self.time = 0
            game.doodler.isBoosted = False
            for b in game.boosters:
                if b == self:
                    game.boosters.remove(b)
                    break
            
    def display(self):
        self.update()
        image(self.img, self.x, self.y, self.w+10, self.h+10)

class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.y_shift = 0
        self.platforms = []
        self.enemies = []
        self.boosters = []
        self.backgroundImage = loadImage(path+"/assets/bck@2x.png")
        self.addPlatforms(8)
        self.doodler = Doodler(self.platforms[0].x, self.platforms[0].y - 100, 35, 50)
        self.score = 0
        self.isStarted = True
        self.level = 0
    
    def addPlatforms(self, n): # adds n times platforms to the game
        for i in range(n-1, -1, -1):
            x = random.randint(0, self.w-80)
            y = (self.h//8)*i
            self.platforms.append(Platform(x, y, 80, 20, "stable"))
    
    def display(self):
        if self.isStarted:
            strokeWeight(0)
            image(self.backgroundImage,0,0)
            for platform in self.platforms:
                platform.display()
            for enemy in self.enemies:
                enemy.display()
            for booster in self.boosters:
                booster.display()
            self.doodler.display()
            platform_manager()
            fill(0, 0, 0)
            textSize(30)
            text("Score: "+str(game.score//100), 20, 40)
            if self.score//100 >= 300:
                self.level = 2
            elif self.score//100 >= 200:
                self.level = 1
            else:
                self.level = 0
                
        else: # the design of game over screen
            background(0)
            fill(255, 255, 255)
            textAlign(CENTER, CENTER)
            textSize(30)
            text("GAME OVER", width/2, 1*height/10)
            textSize(20)
            self.showRecords()
            text("Top Scores:", width/2, 3*height/10)
            text("Score: "+str(game.score//100), width/2, 7.5*height/10)
            text("Retry: [CLICK]", width/2, 8.5*height/10)
            text("Exit: [ESC]", width/2, 9*height/10)
            textAlign(LEFT)
    
    def showRecords(self): # this method reads local file and shows the top results in the game
        records = []
        with open(path + '/records.json') as json_file:
            records = json.load(json_file)['scores']
        if len(records) >= 5:
            for i in range(5):
                text(str(i+1) + '.  ' + str(records[::-1][i]), width/2, (3+(i+1)/1.99)*height/10)
        elif 0 < len(records) < 5:
            for i in range(len(records)):
                text(str(i+1) + '.  ' + str(records[::-1][i]), width/2, (3+(i+1)/1.99)*height/10)
        else:
            pass
    
    def gameOver(self): # the logic of ending the game
        self.isStarted = not self.isStarted
        data = {}
        with open(path + '/records.json') as json_file:
            data = json.load(json_file)
        if self.score//100 != 0:
            data['scores'].append(self.score//100)
            data['scores'] = sorted(data['scores'])
            with open(path+'/records.json', 'w') as outfile:
                json.dump(data, outfile)

game = Game(400, 700)

def platform_manager(): # this method deals with adding/removing platforms, enemies, and booster and chooses different types of platforms/enemies  
    while len(game.platforms) < 9:
        x = random.randint(0, game.w-80)
        y = game.platforms[-1].y - 70
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

    if game.level >= 1 and len(game.enemies) < 2:
        random_value = random.randint(0,100)
        if random_value % 99 == 0:
            possible_coordinates = [game.platforms[-1], game.platforms[-2]]
            coor = random.choice(possible_coordinates)
            x = coor.x 
            y = coor.y-30
            newEnemy = Enemy(0,0,0,0,"")
            if game.level == 1:
                newEnemy = Enemy(x, y, 40, 40, "monster1")
            elif game.level == 2:
                monsterType = random.choice(['monster2', 'monster3', 'monster4', 'monster5', 'monster6', 'monster7', 'monster8', 'monster9'])
                newEnemy = Enemy(x, y, 40, 40, monsterType)
            coor.delegate = newEnemy
            game.enemies.append(newEnemy)
    
    if random.randint(0,130) % 111 == 0 and len(game.boosters) == 0:
        possible_coordinates = [game.platforms[-2], game.platforms[-3]]
        coor = random.choice(possible_coordinates)
        x = coor.x 
        y = coor.y-35
        newBooster = Booster(x,y,30,30,"")
        coor.delegate = newBooster
        game.boosters.append(newBooster)
    
    for p in game.platforms:
        if p.y >= game.h:
            game.platforms.remove(p)
    for e in game.enemies:
        if e.y >= game.h:
            game.enemies.remove(e)
    for b in game.boosters:
        if b.y >= game.h:
            game.boosters.remove(b)

def setup():
    frameRate(40)
    size(game.w, game.h)
    background(255, 255, 255)
    with open(path + '/records.json') as json_file:
        data = json.load(json_file)
        print(data)

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

def mousePressed():
    if not game.isStarted:
        game.isStarted = True
        game.doodler.isBoosted = False
        game.score = 0
        game.platforms = []
        game.boosters = []
        game.enemies = []
        game.addPlatforms(8)
        game.doodler.x = game.platforms[0].x
        game.doodler.y = game.platforms[0].y - 100
        game.doodler.vx = 0
        game.doodler.vy = 0
