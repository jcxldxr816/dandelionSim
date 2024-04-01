import pygame
import time
import random
import math

random.seed()

pygame.init()

W = 480
H = 480
centeredW = W/2
centeredH = H/2

screen = pygame.display.set_mode((W, H))

pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0, W,H))

def drawPixel(x, y,):
    d = pygame.Rect(x, y, 1, 1)
    pygame.draw.rect(screen, (255, 255, 255), d)
    return d

def placeGrassOnCursor(changeGR):
    grassRadius = 20
    grassRadius += changeGR
    if go == False:
        pygame.draw.circle(screen, (22, 196, 30), pygame.mouse.get_pos(), grassRadius)

run = True
go = False

class dandelion:
    def __init__(self, x, y):
        self.xp = x
        self.yp = y
        self.count = 0
        drawPixel(self.xp, self.yp)

dandyList = []
flowerList = []
dandyList.append(dandelion(centeredW, centeredH)) #adding first dandelion
while run == True:

    def generateRandom(): #this function was just for fun, testing out pygame
        a = random.randint(0,W-1)
        b = random.randint(0,H-1)
        drawPixel(a,b)

    def mapFunction(): #this function was just for fun, testing out pygame
        def f(x): ############### CHANGE EQUATION HERE
            y = 3*x +2
            global steep #if multiplying x by val greater than 1, change to True
            steep = False
            return y
        iterations = W
        x = 0 - W/2
        while x < iterations:
            centeredX = x + W/2
            centeredY = f(x) + H/2
            drawPixel(centeredX, centeredY)

            if steep == True: #jerry rigged fix for verticality/AA-esque issues
                drawPixel(centeredX, centeredY+1)
                drawPixel(centeredX, centeredY-1)

            x += 1

#####################################################################################################################

    def wind():
        CHANGE = 20
        global xd, yd
        xd = random.randint(-CHANGE, CHANGE)
        yd = random.randint(-CHANGE, CHANGE)
    
    def dandyFunction(prevList):
        cloneList = []
        forbidden = []
        for d in dandyList:
            cloneList.append(d)
            forbidden.append(d)
        for f in flowerList:
            forbidden.append(f)
        wind()
        for dandy in cloneList:
            variation = random.randint(-5,5)
            nextX = dandy.xp + xd + variation
            variation = random.randint(-5,5)
            nextY = dandy.yp + yd + variation

            #conditions for growth
            noOverlap = True
            for banned in forbidden: #for each existing dandelion/flower/dead flower
                if (nextX == banned.xp) and (nextY == banned.yp):
                    noOverlap = False
                    #continue
            if ((nextX < 0) or (nextY < 0) or (nextX > W) or (nextY > H)) and noOverlap == True:
                noOverlap = False
            if (pygame.Surface.get_at(screen, (int(nextX), int(nextY)))) != (22, 196, 30): #crashes if next point is outside of window
                noOverlap = False

            if noOverlap == True:
                dandyList.append(dandelion(nextX, nextY))

            chance = random.randint(0,1) #chance of blooming/turning yellow
            if chance == 0:
                pygame.draw.rect(screen, (235, 235, 52), pygame.Rect(dandy.xp, dandy.yp, 1, 1))
                flowerList.append(dandy)
                dandyList.remove(dandy) #after spreading seeds, deletes dandelion

        for flower in flowerList: #killing yellow dandelions
            if flower.count >= 50: #lifespan of decaying flower
                pygame.draw.rect(screen, (22, 196, 30), pygame.Rect(flower.xp, flower.yp, 1, 1))
                flowerList.remove(flower)
            if flower.count == 35: #lifespan of flower
                pygame.draw.rect(screen, (99, 92, 57), pygame.Rect(flower.xp, flower.yp, 1, 1))
                flower.count +=1
            else:
                flower.count += 1


    if go == True:
        #generateRandom()
        #mapFunction()
        dandyFunction(dandyList)
        time.sleep(.5)



        #go = False #step by step, use space to advance


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if go == False:
                    go = True
                else:
                    go = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                placeGrassOnCursor(40)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                placeGrassOnCursor(-10)
        if event.type == pygame.MOUSEBUTTONDOWN:
            placeGrassOnCursor(0)

    pygame.display.update()

pygame.quit()