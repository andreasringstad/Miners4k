# import the pygame module, so you can use it
import pygame
import random
import math

running = True

# Create window:
#initialize the pygame module
pygame.init()
pygame.display.set_caption("Miners4K")
clock = pygame.time.Clock()
sprite = pygame.image.load("sprite.png")
pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 20)
message = "Gold: "

# create a surface on the screen that has the size defined under
screenWidth = 640
screenHeight = 500
myDisplay = pygame.display.set_mode((screenWidth,screenHeight))
world = pygame.Surface((screenWidth,screenHeight))
minerSprite = []
circleRadius = 5
circle = pygame.Surface((circleRadius*2,circleRadius*2))
circle.fill((0,0,0))
pygame.draw.circle(circle,(255,255,255),(circleRadius,circleRadius),circleRadius)
circleList = []
for y in range(circleRadius*2):
    for x in range(circleRadius*2):
        if circle.get_at((x,y)) == (255,255,255):
            circleList.append([y,x])
for i in range(20):
    minerSprite.append(sprite.subsurface(i*5,0,5,11))
# Create map
while running: # main loop
    # event handling, gets all event from the event queue
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:
            running = False    
    # level: 0 ground type: 0 air, 1 stone, 2 platform, 3 grass, 4 dirt, 5 gold, 6 surfacegold, 7 dropplatform
    #        color: air-black(0,0,0), stone-gray(140,140,140), filled-dirt(102,68,12), gold(255,255,0), surfacegold(255,255,0)
    
    
    
    # Create Map
    platformWidth = 100
    borderSize = 10
    platformLevel = 150
    platformHeight = 6
    level = []
    for y in range(screenHeight):
        level.append([])
        for x in range(screenWidth):
            level[y].append([0,(0,0,0)]) # Start med full array
            if x < borderSize or x > screenWidth-borderSize: # Langs sidekantene
                level[y][x] = [1,(140,140,140)] # Lag steinkant
            elif platformLevel < y < platformLevel+platformHeight: # Platformnivået, lag enten platform eller gress
                if borderSize <= x < borderSize+platformWidth or screenWidth-borderSize-platformWidth < x <= screenWidth - borderSize: # Lag platform
                    level[y][x] = [2, (140,140,140)]
                else: # Lag gress
                    level[y][x] = [3, (80,140,30)]
            elif y > screenHeight-borderSize:
                level[y][x] = [2, (140,140,140)]
            elif y < platformLevel+platformHeight:
                level[y][x] = [0, (0,0,0)]
            else:
                level[y][x] = [4,random.choice(((135,119,52),(133,107,62),(124,101,47)))]
            
    # Create gold
    for y in range(400,420):
        for x in range(400,420):
            level[y][x] = [5,(255,255,0)]


    for y in range(screenHeight):
        for x in range(screenWidth):
            world.set_at((x,y),level[y][x][1])
    pygame.display.flip()
    draw = [0,0]
    erease = [0,0]
    py = [0,0]
    px = [0,0]
    miners = []
    doAnimation = 0
    goldScore = 0
    goldLeftPlatform = 1
    origin = [platformLevel,borderSize+platformWidth//2]
    goldCurrent = [platformLevel,borderSize+platformWidth//2]
    runningRound = True
    goldTarget = 200
    numberOfMiners = 100
    
    
    
    while runningRound: # main loop
    # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningRound = False
                #running = False
        erease[1] = erease[0]
        draw[1] = draw[0]
        py[1] = py[0]
        px[1] = px[0]
        erease[0], thrash, draw[0] = pygame.mouse.get_pressed(num_buttons=3)
        px[0], py[0] = pygame.mouse.get_pos()
        if erease[0]:
            if erease[1]:
                if py[0] != py[1] or px[0] != px[1]:
                    current = [py[0],px[0]]
                    floatModifier = 0
                    floatNumber = 0
                    if py[0] > py[1]:
                        pyDifference = py[0]-py[1]
                        pyModifier = 1
                    else:
                        pyDifference = py[1]-py[0]
                        pyModifier = -1
                    if px[0] > px[1]:
                        pxDifference = px[0]-px[1]
                        pxModifier = 1
                    else:
                        pxDifference = px[1]-px[0]
                        pxModifier = -1
                    if pyDifference > pxDifference:
                        floatModifier = pxDifference/pyDifference
                        floatNumber = current[1]
                        for i in range(pyDifference-pxDifference):
                            for i in range(len(circleList)):
                                if level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius][0] == 4 or level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius][0] == 3:
                                    level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius] = [0,(0,0,0)]
                                    world.set_at((circleList[i][1]+current[1]-circleRadius,circleList[i][0]+current[0]-circleRadius),level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius][1])
                            current[0] += pyModifier
                            floatNumber += floatModifier
                            current[1] = round(floatNumber)
                    else:
                        floatModifier = pyDifference/pxDifference
                        floatNumber = current[0]
                        for i in range(pxDifference-pyDifference):
                            for i in range(len(circleList)):
                                if level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius][0] == 4 or level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius][0] == 3:
                                    level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius] = [0,(0,0,0)]
                                    world.set_at((circleList[i][1]+current[1]-circleRadius,circleList[i][0]+current[0]-circleRadius),level[circleList[i][0]+current[0]-circleRadius][circleList[i][1]+current[1]-circleRadius][1])
                            current[1] += pxModifier
                            floatNumber += floatModifier
                            current[0] = round(floatNumber)



            else:
                for i in range(len(circleList)):
                    if level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius][0] == 4 or level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius][0] == 3:
                        level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius] = [0,(0,0,0)]
                        world.set_at((circleList[i][1]+px[0]-circleRadius,circleList[i][0]+py[0]-circleRadius),level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius][1])

        if draw[0]:
            for i in range(len(circleList)):
                if level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius][0] == 0:
                    level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius] = [4,(124,91,68)]
                    world.set_at((circleList[i][1]+px[0]-circleRadius,circleList[i][0]+py[0]-circleRadius),level[circleList[i][0]+py[0]-circleRadius][circleList[i][1]+px[0]-circleRadius][1])


        myDisplay.blit(world,(0,0))
        if doAnimation == 3:
            doAnimation = 0
        doAnimation += 1
        
        # Spawn miners
        if numberOfMiners > 0:
            miners.append([1,-10,random.randint(10,90),1,-1,1,0,1])#miners: 0 alive, 1 y, 2 x, 3 state(0ground, 1 falling, 2 jump1, 3 jump2, 4 jump3, 5 jump4), 4 facing, 5 carrying gold, 6 animation, 7 animation +/-
            numberOfMiners -= 1
        
        
        # Behandle miners
        for i in range(len(miners)):
            aroundMiner = [level[miners[i][1]+11][miners[i][2]+2],level[miners[i][1]+12][miners[i][2]+2],level[miners[i][1]+10][miners[i][2]+2+2*miners[i][4]][0]]
            if miners[i][0] == 1: # Hvis han lever:
                
                if miners[i][5] == 0: # Check if miner found gold
                    if level[miners[i][1]+11][miners[i][2]+2][0] == 5:
                        miners[i][5] = 1
                        level[miners[i][1]+11][miners[i][2]+2] = [0,(0,0,0)]
                        world.set_at((miners[i][2]+2,miners[i][1]+11),(0,0,0))
                    elif level[miners[i][1]+10][miners[i][2]+2+miners[i][4]][0] == 5:
                        miners[i][5] = 1
                        level[miners[i][1]+10][miners[i][2]+2+miners[i][4]] = [0,(0,0,0)]
                        world.set_at((miners[i][2]+2+miners[i][4],miners[i][1]+11),(0,0,0))
                else:
                    if miners[i][1]+10 == platformLevel:
                        if miners[i][2] == borderSize+platformWidth//2:
                            miners[i][5] = 0
                            goldScore += 1
                            if goldCurrent[0] == origin[0] and goldCurrent[1] == origin[1]: 
                                    level[origin[0]][origin[1]] == [0,(255,255,0)]
                                    world.set_at((origin[1],origin[0]),(255,255,0))
                                    goldCurrent[1] -= 1
                            else:
                                level[goldCurrent[0]][goldCurrent[1]] == [0,(255,255,0)]
                                world.set_at((goldCurrent[1],goldCurrent[0]),(255,255,0))
                                if goldCurrent[1] == origin[1]-goldLeftPlatform:
                                    if goldCurrent[0] == origin[0]-goldLeftPlatform:
                                        goldCurrent[1] += 1
                                    else:
                                        goldCurrent[0] -= 1
                                elif goldCurrent[0] == origin[0]-goldLeftPlatform:
                                    if goldCurrent[1] == origin[1]+goldLeftPlatform:
                                        goldCurrent[0] +=1
                                    else:
                                        goldCurrent[1] += 1
                                else:
                                    if goldCurrent[0] == origin[0]:
                                        goldCurrent[1] -= goldLeftPlatform*2+1
                                        goldLeftPlatform +=1
                                    else:
                                        goldCurrent[0] += 1
                                    
                                

                        elif miners[i][2] == screenWidth-borderSize-platformWidth//2:
                            miners[i][5] = 0
                            goldScore += 1
                            #Platform needs to take care of the gold



                if miners[i][3] == 1: # Hvis han faller:
                    miners[i][6] == 0
                    if level[miners[i][1]+11][miners[i][2]+2][0] != 0: # Hvis det er bakke rett under ham:
                        miners[i][3] = 0 # Er han "grounded"
                    else: # Om ikke, faller han en ned:
                        miners[i][1] += 1
                    # Draw miner
                    if miners[i][4] == 1: # Hvis han ser mot høyre:
                        if miners[i][5] == 0: # Hvis han ikke har gull:
                            myDisplay.blit(minerSprite[0], (miners[i][2],miners[i][1])) # Faller og ser mot høyre uten gull
                        else: # Hvis han ikke har gull
                            myDisplay.blit(minerSprite[5], (miners[i][2],miners[i][1])) # Faller og ser mot høyre med gull
                    elif miners[i][5] == 0: # Ellers ser han mot venstre, og hvis han ikke har gull
                        myDisplay.blit(minerSprite[10], (miners[i][2],miners[i][1]))     # Faller og ser mot venstre uten gull
                    else:
                        myDisplay.blit(minerSprite[15], (miners[i][2],miners[i][1]))     # Faller og ser mot venstre med gull


                elif miners[i][3] == 0:   # Hvis han er grounded
                    if level[miners[i][1]+10][miners[i][2]+2+2*miners[i][4]][0] == 0: # Hvis det er luft foran føttene så:
                        miners[i][2] += miners[i][4]                                    # Går han et steg fremover
                    elif level[miners[i][1]+9][miners[i][2]+2+2*miners[i][4]][0] == 0: # Hvis det er luft en foran og en opp så:
                        miners[i][2] += miners[i][4]
                        miners[i][1] -= 1
                    elif level[miners[i][1]+8][miners[i][2]+2+2*miners[i][4]][0] == 0: # Hvis det er luft en foran og to opp så:
                        miners[i][2] += miners[i][4]
                        miners[i][1] -= 2
                    elif level[miners[i][1]+8][miners[i][2]+2+2*miners[i][4]][0] == 0: # Hvis det er luft en foran og to opp så:
                        miners[i][2] += miners[i][4]
                        miners[i][1] -= 1
                    elif level[miners[i][1]+11][miners[i][2]+2+2*miners[i][4]][0] == 0: # Hvis det 
                        miners[i][2] += miners[i][4]
                        miners[i][1] += 1
                    # Fix: Må kanskje ha med en sjekk for å gå 2 opp.
                    else:
                        if random.randint(0,1) > 0:
                            miners[i][4] *= -1
                            miners[i][3] = 18
                        else:
                            miners[i][4] *= -1
                     

                    if level[miners[i][1]+11][miners[i][2]+2][0] == 0: # Hvis Det er luft rett under ham
                        if level[miners[i][1]+12][miners[i][2]+2][0] == 0: # Hvis Det er luft 2 under ham
                            if level[miners[i][1]+13][miners[i][2]+2][0] == 0: # Hvis Det er luft 2 under ham
                                if random.randint(0,1) > 0: # Fix: her må vi sjekke at det er rom får å hoppe.
                                    miners[i][3] = 18
                                else:
                                    miners[i][3] = 1
                            else: # Hvis det bare er to pixler med luft under ham
                                miners[i][1] += 1
                                miners[i][3] = 1
                        else: # Hvis det bare er en pixel med luft under ham
                            miners[i][1] += 1
                    # Her må det være mange flere sjekker:
                        # Om han går fremover og bakken går "litt" nedover må han også gå nedover
                        # Om han går fremover og bakken går "litt" oppover må han også gå oppover
                        # Om han går fremover og bakken går "veldig" nedover begynner han å falle (state = falling), eller gjøre et hopp fremover
                        # Om han går fremover og han møter en vegg, må han snu, vente litt og enten hoppe eller bare gå

                    # Draw miner
                    if miners[i][4] == 1: # Hvis han ser mot høyre:
                        if miners[i][5] == 0:# Hvis han ikke har gull:
                            myDisplay.blit(minerSprite[miners[i][6]], (miners[i][2],miners[i][1])) # Går mot høyre uten gull
                        else: # Hvis han ikke har gull
                            myDisplay.blit(minerSprite[miners[i][6]+5], (miners[i][2],miners[i][1])) # Går mot høyre med gull
                    elif miners[i][5] == 0: # Ellers ser han mot venstre, og hvis han ikke har gull
                        myDisplay.blit(minerSprite[miners[i][6]+10], (miners[i][2],miners[i][1]))     # Går mot venstre uten gull
                    else:
                        myDisplay.blit(minerSprite[miners[i][6]+15], (miners[i][2],miners[i][1]))     # Går mot venstre med gull
                    if miners[i][6] == 0:
                        miners[i][7] = 1
                    elif miners[i][6] == 4:
                        miners[i][7] = -1
                    if doAnimation == 1:
                        miners[i][6] += miners[i][7]
                    
                else:
                    if miners[i][3] > 9:
                        if level[miners[i][1]+9][miners[i][2]+2+miners[i][4]][0] == 0: # Om det er luft en foran en opp så flytt ham dit
                            miners[i][1] -= 1
                            miners[i][2] += miners[i][4]
                        elif level[miners[i][1]+10][miners[i][2]+2+miners[i][4]][0] == 0: # Om det bare er luft foran ham, flytt han en frem
                            miners[i][2] += miners[i][4]
                        elif level[miners[i][1]+9][miners[i][2]+2][0] == 0:
                            miners[i][1] -= 1
                        else:
                            miners[i][3] == 1
                        miners[i][6] == 2

                    elif miners[i][3] > 5:
                        if level[miners[i][1]+10][miners[i][2]+2+miners[i][4]][0] == 0: # Om det er luft en foran ham, flytt han fram
                            miners[i][2] += miners[i][4]
                        else:
                            miners[i][3] == 1
                        miners[i][6] == 2
                    else:
                        if level[miners[i][1]+11][miners[i][2]+2+miners[i][4]][0] == 0:
                            miners[i][1] += 1
                            miners[i][2] += miners[i][4]
                        miners[i][6] = 0
                    miners[i][3] -= 1

                    # Draw Jumping miner
                    if miners[i][4] == 1: # Hvis han ser mot høyre:
                        if miners[i][5] == 0:# Hvis han ikke har gull:
                            myDisplay.blit(minerSprite[miners[i][6]], (miners[i][2],miners[i][1])) # Hopper mot høyre uten gull
                        else: # Hvis han ikke har gull
                            myDisplay.blit(minerSprite[miners[i][6]+5], (miners[i][2],miners[i][1])) # Hopper mot høyre med gull
                    elif miners[i][5] == 0: # Ellers ser han mot venstre, og hvis han ikke har gull
                        myDisplay.blit(minerSprite[miners[i][6]+10], (miners[i][2],miners[i][1]))     # Hopper mot venstre uten gull
                    else:
                        myDisplay.blit(minerSprite[miners[i][6]+15], (miners[i][2],miners[i][1]))     # Hopper mot venstre med gull
        scoreMessage = message + str(goldScore) + "/" + str(goldTarget)
        textsurface = myfont.render(scoreMessage, False, (255,255,255))
        myDisplay.blit(textsurface,(borderSize+2,0))
        pygame.display.update()
        clock.tick(35)


"""        # First set up the variables for the current level
        screenWidth = current_level / 4 * 384 + 640
        if current_level>1:
            screenHeight = 1024
        else:
            screenHeight = 480
        level_rocks = (current_level - 1) / 2 * 100
        level_target = current_level * 500
        level_diggers = current_level * current_level * 50
        level_goldLumps = current_level * current_level * 50

        # Special levels that don't confomr to the formulas
        if current_level == 0:
            level_rocks = 0
            level_target = 100
            level_diggers = 50
            level_goldLumps = 10
        
        if current_level == 1:
            level_rocks = 10
            level_target = 200
            level_goldLumps = 30

        if current_level == 2:
            level_rocks = 50

        if current_level == 6:
            screenHeight = 2048
            level_target = 99999
            level_diggers = 800

        level_timeLimit = level_target * 2
"""
