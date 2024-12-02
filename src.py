from cmu_graphics import *
import math
import copy

def onAppStart(app):
    #all images and data from colormax.org

    app.testImage ='test2.png'

    app.correctAnswers = [7, 6, 26,15,6,73,5,16,45,12,29,8]
    app.alternateAnswers = [
    (0,), (0,), (6, 2), (17,), (0,), (0,), (0,), (0,), (0,), (0,), (70,), (3, 0)
    ]
    app.tempMeaning = [
    ("colorblind",), ("colorblind",), ("red-green",), ("colorblind",), 
    ("colorblind",), ("colorblind",), ("colorblind",), ("colorblind",), 
    ("colorblind",), ("red-green",), ("red-green",)
    ]
    app.answerMeaning = [
    (None,), (None,), ("red", "green"), ("red-green",), (None,), (None,), 
    (None,), (None,), (None,), (None,), ("red-green",), ("red-green",)
    ]

    app.d = {"colorblind": 0, "red-green":0}
    app.expr = ""
    app.countAnswered = 1
    app.guesses = []

    app.redY = 350
    app.greenY = 500
    app.blueY = 650
    app.blueCircle = False
    app.redCircle = False
    app.greenCircle = False
    app.radius = 10
    app.lineMin = 10
    app.lineMax = 265
    app.changeRed = 0
    app.changeGreen = 0 
    app.changeBlue = 0
    app.center = (app.lineMin+app.lineMax)//2
    app.redX = app.center
    app.greenX = app.center
    app.blueX = app.center
    app.p1x = 0
    app.p1y = 0
    app.p2x = 0
    app.p2y = 0
    app.p1 = False  
    app.colorBlindnessType = "none"
    app.redGreen = False
    app.blueYellow = False

    #the following code ingests a txt file of a 2d array that is not comma seperate, but line seperated, and turns it into a usable array
    #note that the sample inputs currently in txt files are obtained from chat gpt's mobile app. I inputted an image and requested chatGPT to return a 2d array of rgb values as tuples. This is something that can be done using various websites as well.
    filePath = "rgbArraySmaller.txt"  # Path to the image
    app.hsv = []
    app.enhanced = []
    app.border = []
    app.originalRgb = []
    
    app.startX, app.startY = 300, 50
    n = 10000000000000000 
    app.setMaxShapeCount(n)

def test_redrawAll(app):
    if(app.countAnswered<=12):
        drawImage(app.testImage, 0,0)
        
        drawLabel(f"Type in the number you see in circle {app.countAnswered}", 1200, 50, size = 20)
        drawLabel(str(app.expr),1200, 75, size = 20)


def test_onKeyPress(app, key):
    if(key.isdigit()):
        app.expr+=key
    if(key == "enter" and app.countAnswered<=12 and app.expr != ""):
        app.guesses.append(int(app.expr))
        app.expr = ""
        app.countAnswered+=1
    elif(key=='backspace' and app.expr!=""):
        app.expr = app.expr[0:len(app.expr)-1]
    #this next line is here temporarily because i do not know how to access app from main
    if app.countAnswered >=12:
        generalColorBlindness, redGreen = checkResults(app)
        if redGreen > 0 and generalColorBlindness>0:
            app.colorBlindnessType = "both"
        elif redGreen == 0 and generalColorBlindness>0:
            app.colorBlindnessType = "blue-yellow"
        elif redGreen >0 and generalColorBlindness==0:
            app.colorBlindnessType = "red-green"
        setActiveScreen("results")


def evaluatedExpr(expr):
    firstNum = int(expr[0:expr.find("+")])
    secondNum = int(expr[expr.find("+")+1:len(expr)])
    return expr + "=" + str(firstNum+secondNum)

def checkResults(app):
    for i in range (len(app.guesses)):
        if int(app.guesses[i]) == app.correctAnswers[i]:
            continue
        else:
            for j in range(len(app.alternateAnswers[i])):
                if int(app.guesses[i]) == app.alternateAnswers[i][j]:
                    app.d[app.tempMeaning[i][0]] = app.d.get(app.tempMeaning[i][0],0)+1
    return app.d["colorblind"], app.d["red-green"]

def results_redrawAll(app):
    generalColorBlindness, redGreen = checkResults(app)
    if redGreen > 0 and generalColorBlindness>0:
        drawLabel("You have red-green and blue-yellow colorblindness", app.width/2, app.height/2, size = 40)
    elif redGreen == 0 and generalColorBlindness>0:
        drawLabel("You have blue-yellow colorblindness", app.width/2, app.height/2, size = 40)
    elif redGreen >0 and generalColorBlindness==0:
        drawLabel("You have red-green colorblindness", app.width/2, app.height/2, size = 40)
    else:
        drawLabel("You are not colorblind, but feel free to proceed to see the transformations", app.width/2, app.height/2, size = 40)

    drawLabel("Enter the path below", app.width/2, app.height/2+40, size = 15)
    drawLabel(str(app.expr),app.width/2, app.height/2+60, size = 15)

    drawLabel("Click enter to continue", app.width/2, app.height/2+80, size = 20)

def results_onKeyPress(app, key):
    
    if(key=='backspace' and app.expr!=""):
        app.expr = app.expr[0:len(app.expr)-1]
    elif key == 'enter':
        app.filePath = app.expr
        with open(app.filePath, "r") as f:
            for line in f:
                row = eval(line.strip())
                app.originalRgb.append(row)
        app.enhanced = enhanceForColorblindness(app)
        app.border = findHueBorder(app.originalRgb, 30)
        setActiveScreen('transformedImageWithSliders')
    elif key!=" ":
        app.expr+=key


def transformedImageWithSliders_redrawAll(app):
    drawLine(app.lineMin,app.blueY, app.lineMax, app.blueY)
    drawCircle(app.blueX, app.blueY,  app.radius, fill = 'blue')
    drawLine(app.lineMin,app.greenY, app.lineMax, app.greenY)
    drawCircle(app.greenX, app.greenY,  app.radius, fill = 'green')
    drawLine(app.lineMin,app.redY, app.lineMax, app.redY)
    drawCircle(app.redX, app.redY,  app.radius, fill = 'red')

    x = app.startX
    y = app.startY
    rectWidth = 10
    rectHeight = 10

    for i in range(len(app.enhanced)):
        x = app.startX  # Reset x for each new row
        for j in range(len(app.enhanced[i])):
            r, g, b = app.enhanced[i][j]
            if r+app.changeRed>255:
                r = 255
            elif r+app.changeRed<0:
                r = 0
            else:
                r += app.changeRed
            if g+app.changeGreen>255:
                g = 255
            elif g+app.changeGreen<0:
                g = 0
            else:
                g+=app.changeGreen
            if b+app.changeBlue>255:
                b = 255
            elif b+app.changeBlue<0:
                b= 0
            else:
                b+=app.changeBlue
            drawRect(x, y, rectWidth, rectHeight, fill=rgb(r, g, b))
            if app.border[i][j]:
                drawRect(x,y,rectWidth, rectHeight, fill = 'black')
            x += rectWidth
        y += rectHeight
    
    if app.p1:
        drawCircle(app.p1x, app.p1y, 1, fill = 'black')
    if app.p1 and app.p2:
        drawCircle(app.p2x, app.p2y, 1, fill = 'black')

# the following function checks which of the sliders are chosen and only moves them if they are chosen.
def transformedImageWithSliders_onMousePress(app, mouseX, mouseY):
    if distance(mouseX, app.blueX, mouseY, app.blueY)< app.radius:
        app.blueCircle = not app.blueCircle
        app.redCircle = False
        app.greenCircle = False
    elif distance(mouseX, app.greenX, mouseY, app.greenY)< app.radius:
        app.greenCircle = not app.greenCircle
        app.redCircle = False
        app.blueCircle = False
    elif distance(mouseX, app.redX, mouseY, app.redY)< app.radius:
        app.redCircle = not app.redCircle
        app.blueCircle = False
        app.greenCircle = False
    
#the following function moves the slider circle and adjusts the rgb values, ensuring they dont go bellow 0 and over 255
def transformedImageWithSliders_onMouseMove(app, mouseX, mouseY):
    if app.blueCircle:
        if mouseX > app.lineMax:
            app.blueX = app.lineMax
        elif mouseX<app.lineMin:
            app.blueX = app.lineMin
        else:
            app.blueX = mouseX

        app.changeBlue = (app.blueX - app.center)*2
    if app.greenCircle:
        if mouseX > app.lineMax:
            app.greenX = app.lineMax
        elif mouseX<app.lineMin:
            app.greenX = app.lineMin
        else:
            app.greenX = mouseX
        app.changeGreen = (app.greenX - app.center)*2
    if app.redCircle:
        if mouseX > app.lineMax:
            app.redX = app.lineMax
        elif mouseX<app.lineMin:
            app.redX = app.lineMin
        else:
            app.redX = mouseX
        app.changeRed = (app.redX - app.center)*2


def distance(x1,x2, y1, y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

"""
The idea to use the following transformation scheme of hsv came from a conversation with my father, Vivek Sanghi, who was aware that I was working on this project.

We initially thought it would be a good idea to do edge detection, for which I have left in commented code. The initial idea was to try and detect when there were severe changes in intensity of colors or in rgb values and outline those areas, however, this was not sufficient.
Further reserach led to HSV and RGB transformation which explored using few key sources:

1. This source discusses how HSV is used to depict the way humans percieve combinations of colors, rather than rgb which focuses more on individual colors. It also includes information on which hues map to which colors which is essential for the enhance colors function: https://www.lifewire.com/what-is-hsv-in-design-1078068
2. The following source is used to figure out how to transform values from RGB to HSV, which is used in the enhance colors function and is implemented below: https://www.rapidtables.com/convert/color/rgb-to-hsv.html
3. The following source is used to figure out how to transform values from HSV to RGB, which is used in the enhance colors function and is implemented below: https://www.rapidtables.com/convert/color/hsv-to-rgb.html
"""

def rgbToHsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    maxC = max(r, g, b)
    minC = min(r, g, b)
    delta = maxC - minC

    if delta == 0:
        h = 0
    elif maxC == r:
        h = (60 * ((g - b) / delta) + 360) % 360
    elif maxC == g:
        h = (60 * ((b - r) / delta) + 120) % 360
    elif maxC == b:
        h = (60 * ((r - g) / delta) + 240) % 360
    
    if maxC == 0:
        s = 0
    else:
        s = delta / maxC
    
    v = maxC
    
    return h, s, v

def hsvToRgb(h, s, v):
    c = v * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = v - c
    
    if 0 <= h < 60:
        rp, gp, bp = c, x, 0
    elif 60 <= h < 120:
        rp, gp, bp = x, c, 0
    elif 120 <= h < 180:
        rp, gp, bp = 0, c, x
    elif 180 <= h < 240:
        rp, gp, bp = 0, x, c
    elif 240 <= h < 300:
        rp, gp, bp = x, 0, c
    else:
        rp, gp, bp = c, 0, x
    
    r = int((rp + m) * 255)
    g = int((gp + m) * 255)
    b = int((bp + m) * 255)
    
    return r, g, b

def enhanceForColorblindness(app):
    adjustedImage = []
    if app.colorBlindnessType == "both":
        app.redGreen = True 
        app.blueYellow = True
    elif app.colorBlindnessType == "red-green":
        app.redGreen = True 
    elif app.colorBlindnessType == "blue-yellow":
        app.blueYellow = True

    for row in app.originalRgb:
        adjustedRow = []
        for r, g, b in row:
            h, s, v = rgbToHsv(r, g, b)
            
            # Adjust for red and green hues - addressing red-green colorblindness
            if ((0 <= h < 60) or (300 <= h < 360)):  # Red and magenta hues
                # Shift reds to blue (around 270)
                h = 270
            elif 120 <= h < 180:  # Green hues
                # Shift greens to yellow (around 90)
                h = 90

            #Adjust for blue and yellow hues - addressing blue-yellow colorblindness
            elif (240 <= h < 300):
                #Shift blues to cyans (around 210)
                h = 210
            elif(60 <= h < 120):
                h = 30

            newR, newG, newB = hsvToRgb(h, s, v)
            adjustedRow.append((newR, newG, newB))
        
        adjustedImage.append(adjustedRow)
    
    return adjustedImage

def detectBorder(app):
    #this function should use backtracking to go through all the hues and find the border based on a certain threshold that can be adjusted with one more slider
    drawLabel("hi", 10, 10)

"""
The idea for the following recursive approach came from a conversation with my TP Mentor, Angie Chi (achi2), who shared that I could explore a flood fill algorithm to detect borders
I did some more research and brainstorming on ways to do border detection recursively and found the DFS algorithm, which is much like backtracking, but has no condition in which it terminates, because there is no condition under which it terminates.
This algorithm made sense in this use case, since there is no standard case in which the algorithm should terminate.
I used the following source to develop a better understanding: https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/
The implementation below is entirely my own as can be see by the clear backtracking approach I have applied as taught during 112 lectures in class
The increeased efficiency below is highlighted further, but generally, the following algorithm finds pixels that are considered "borders" based on a moveable threshold,
and then searchers the neighbors. This is more efficient than just going through every pixel and checking all 8 of its neighbors, since going from one pixel to another recursively does not required us to check
8*the number of pixels.
"""
#the following function is meant to help find the borders of objects, making them even clearer 
def findHueBorder(rgbArray, hueThreshold):
    hsvArray = [[rgbToHsv(r, g, b) for r, g, b in row] for row in rgbArray]
    #the following lines initialize the arrays we will use to keep track of the border and where we have been
    rows, cols = len(hsvArray), len(hsvArray[0])
    seen = [[False for _ in range(cols)] for _ in range(rows)]
    border = [[False for _ in range(cols)] for _ in range(rows)]
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  
    
    #the following code works because hue's wrap around in values back to 360, so rather than there being a diffence of 340 between 10 and 350, there is actually a difference of 20
    def isBorder(hue, newHue):
        diff = abs(hue - newHue)
        return min(diff, 360 - diff) > hueThreshold
    
    #the following function goes determines whether a startpoint is a border, and then goes down the tree to determine if the border continues. This is most efficient, because it is likely that one border pixel has other border pixels around it
    def backtrack(row, col):
        seen[row][col] = True
        hue, x, y = hsvArray[row][col]
        
        borderPixel = False
        for nextR, nextC in directions:
            currR, currC = row + nextR, col + nextC
            if 0 <= currR < rows and 0 <= currC < cols and not seen[currR][currC]:
                newHue, p, q = hsvArray[currR][currC]
                if isBorder(hue, newHue):
                    borderPixel = True
                    backtrack(currR, currC)
        
        border[row][col] = borderPixel
    #the following loop goes through all the elements, but wil often not have to check because the backtracking step above will determine large groups of border recursively
    for i in range(rows):
        for j in range(cols):
            if not seen[i][j]:
                backtrack(i, j)
    
    return border


def main():
    runAppWithScreens(initialScreen='test')

   
main()
