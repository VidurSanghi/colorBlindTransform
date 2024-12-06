from cmu_graphics import *
import math
import copy
from PIL import Image
import numpy as np

def onAppStart(app):

    #all test images and data from colormax.org
    app.testImage ='test2.png'

    app.correctAnswers = [7, 6, 26, 15, 6, 73, 5, 16, 45, 12, 29, 8]
    app.tempMeaning = [
    "colorblind", "colorblind", "red-green", "colorblind", 
    "colorblind", "colorblind", "colorblind", "colorblind", 
    "colorblind", "red-green", "red-green", "red-green"
]

    app.saved = False
    app.d = {"colorblind": 0, "red-green":0}
    app.expr = ""
    app.countAnswered = 1
    app.guesses = []
    app.threshold2Value = 20
    app.redY = 250
    app.greenY = 375
    app.blueY = 500
    app.thresholdY = 625
    app.threshold2Y = 750
    app.optionsY = 840

    app.blueCircle = False
    app.redCircle = False
    app.greenCircle = False
    app.threshold = False
    app.threshold2 = False

    app.radius = 10
    app.lineMin = 50
    app.lineMax = 305
    app.changeRed = 0
    app.changeGreen = 0 
    app.changeBlue = 0
    app.changeThreshold = 0
    app.center = (app.lineMin+app.lineMax)//2
    app.redX = app.center
    app.greenX = app.center
    app.blueX = app.center
    app.thresholdX = app.center
    app.threshold2X = app.center
    app.redGreen = True
    app.blueYellow = True
    app.error = False
    app.floodArr = []
    app.flooded = False
    app.hsv = []
    app.enhanced = []
    app.border = []
    app.originalRgb = []
    app.startX, app.startY = 500, 30
    n = 10000000000000000 
    app.setMaxShapeCount(n)
    app.fillThreshold = 20
    app.floodX = 0
    app.floodY = 0

def start_redrawAll(app):
    drawRect(0, 0, 2000, 2000, fill=rgb(41,189,193))
    drawLabel("Colorblind Transformation", app.width/2, app.height/2-300, size = 80)
    drawLabel("The purpose of this tool is to help colorblind people distinguish objects in images that can be difficult to see", app.width/2, app.height/2-20, size = 30)
    drawLabel("This project focuses on red-green (Deuteranomaly) and blue-yellow (Tritanomaly) colorblindness, and starts with a short assesment", app.width/2, app.height/2+30, size = 20)
    drawLabel("Please click enter (return) to begin the assesment", app.width/2, app.height/2+60, size = 18)

    drawRect(30, 900, 70,30, fill = "black")
    drawLabel("Next Page", 65, 915, fill = "white")

def start_onKeyPress(app, key):
    if key == "enter":
        setActiveScreen("test")

def start_onMousePress(app, mouseX, mouseY):
    if mouseX>30 and mouseX< 100 and mouseY>900 and mouseY<930:
        setActiveScreen("test")

def test_onMousePress(app, mouseX, mouseY):
    if mouseX>30 and mouseX< 100 and mouseY>900 and mouseY<930:
        setActiveScreen("results")


def test_redrawAll(app):
    drawRect(30, 900, 70,30, fill = "black")
    drawLabel("Skip Test", 65, 915, fill = "white")

    if(app.countAnswered<13):
        drawImage(app.testImage, 0,0)
        
        drawLabel(f"Type in the number you see in circle {app.countAnswered}", 1200, 50, size = 20)
        drawLabel(str(app.expr),1200, 75, size = 20)
        drawLabel("Press return (enter) to submit your answer", 1200, 100, size = 15)

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
    if app.countAnswered >12:
        generalColorBlindness, redGreen = checkResults(app)
        if redGreen == 0 and generalColorBlindness>0:
            app.redGreen = False
        elif redGreen >0 and generalColorBlindness==0:
            app.blueYellow = False
        elif redGreen == 0 and generalColorBlindness == 0:
            app.blueYellow = False
            app.redGreen = False
        setActiveScreen("results")

def evaluatedExpr(expr):
    firstNum = int(expr[0:expr.find("+")])
    secondNum = int(expr[expr.find("+")+1:len(expr)])
    return expr + "=" + str(firstNum+secondNum)

def checkResults(app):
    if len(app.guesses)<12:
        return 0,0
    for i in range (len(app.guesses)):
        if int(app.guesses[i]) == app.correctAnswers[i]:
            continue
        else:
            app.d[app.tempMeaning[i]] +=1
    return app.d["colorblind"], app.d["red-green"]

def results_redrawAll(app):
    drawRect(30, 900, 70,30, fill = "black")
    drawLabel("Next Page", 65, 915, fill = "white")

    #the background rgb value was chosen from the following website: https://www.color-hex.com/color-palette/10449
    
    drawRect(0, 0, 2000, 2000, fill=rgb(41,189,193))
    generalColorBlindness, redGreen = checkResults(app)
    if redGreen > 0 and generalColorBlindness>0:
        drawLabel("You have red-green and blue-yellow colorblindness", app.width/2, app.height/2-100, size = 50)
    elif redGreen == 0 and generalColorBlindness>0:
        drawLabel("You have blue-yellow colorblindness", app.width/2, app.height/2-100, size = 50)
    elif redGreen >0 and generalColorBlindness==0:
        drawLabel("You have red-green colorblindness", app.width/2, app.height/2-100, size = 50)
    else:
        drawLabel("We could not determine what kind of colorblindness you have!",  app.width/2, app.height/2-100, size = 40)

    drawLabel("Please enter a file path to the image you want to transform below", app.width/2, app.height/2-35, size = 20)
    drawLabel(str(app.expr),app.width/2, app.height/2-5, size = 20)

    drawLabel("Click enter to continue", app.width/2, app.height/2+25, size = 20)
    if app.error: 
        drawLabel("File not found, please try another path", app.width/2, app.height/2+45, size = 20, fill = 'red')

#the  code for the next 2 functions, saveRgbArray and saveRgbArrayAsPng, is produced with the help of chatGPT and my own work.

def saveRgbArray(image_path, output_file):
    image = Image.open(image_path)
    image = image.resize((min(image.width, 64), min(image.height, 64)))
    image = image.convert('RGB')
    rgb_array = np.array(image)
    with open(output_file, 'w') as f:
        for row in rgb_array:
            row_str = ', '.join([f"({r},{g},{b})" for r, g, b in row])
            f.write(f"[{row_str}]\n")

def saveRgbArrayAsPng(rgb_array, mask_array, overlay_mask_array, output_file):
    height = len(rgb_array)
    width = len(rgb_array[0])

    if len(mask_array) != height or any(len(row) != width for row in mask_array):
        raise ValueError("Mask array dimensions must match the RGB array dimensions.")
    if len(overlay_mask_array) != height or any(len(row) != width for row in overlay_mask_array):
        raise ValueError("Overlay mask array dimensions must match the RGB array dimensions.")
    
    modified_array = [
        [
            (0, 0, 0) if mask_array[row][col] else rgb_array[row][col]
            for col in range(width)
        ]
        for row in range(height)
    ]
    
    for row in range(height):
        for col in range(width):
            if overlay_mask_array[row][col]:
                modified_array[row][col] = (255, 255, 0)  # Yellow color

    image = Image.new("RGB", (width, height))
    image.putdata([pixel for row in modified_array for pixel in row])  # Flatten the list of rows into a single list
    image.save(output_file)

#the purpose of the try and catch below is to be able to detect if a user inputs an invalid file path, and notify them rather than crashing.
def results_onKeyPress(app, key):
    
    if(key=='backspace' and app.expr!=""):
        app.expr = app.expr[0:len(app.expr)-1]
    elif key == 'enter' and app.expr!="" and app.expr!= " ":
        try:
            app.filePath = app.expr+"1"
            saveRgbArray(app.expr, app.filePath)
            with open(app.filePath, "r") as f:
                for line in f:
                    row = eval(line.strip())
                    app.originalRgb.append(row)
            app.enhanced = enhanceForColorblindness(app)
            app.border = findHueBorder(app.originalRgb, 30)
            setActiveScreen('transformedImageWithSliders')
        except FileNotFoundError:
            app.error = True
            app.expr = ""
        except IsADirectoryError:
            app.error = True
            app.expr = ""
        except Exception as e:
            app.error = True
            app.expr = ""

    elif key!=" " and key!= "backspace" and key!="enter":
        app.expr+=key

def results_onMousePress(app, mouseX, mouseY):
    if mouseX>30 and mouseX< 100 and mouseY>900 and mouseY<930 and app.expr != "" and app.expr!= " ":
        try:
            app.filePath = app.expr+"1"
            saveRgbArray(app.expr, app.filePath)
            with open(app.filePath, "r") as f:
                for line in f:
                    row = eval(line.strip())
                    app.originalRgb.append(row)
            app.enhanced = enhanceForColorblindness(app)
            app.border = findHueBorder(app.originalRgb, 30)
            setActiveScreen('transformedImageWithSliders')
        except FileNotFoundError:
            app.error = True
            app.expr = ""
        except IsADirectoryError:
            app.error = True
            app.expr = ""
        except Exception as e:
            app.error = True
            app.expr = ""

def transformedImageWithSliders_redrawAll(app):
    
    drawLine(app.lineMin,app.blueY, app.lineMax, app.blueY)
    drawCircle(app.blueX, app.blueY,  app.radius, fill = 'blue')
    drawLine(app.lineMin,app.greenY, app.lineMax, app.greenY)
    drawCircle(app.greenX, app.greenY,  app.radius, fill = 'green')
    drawLine(app.lineMin,app.redY, app.lineMax, app.redY)
    drawCircle(app.redX, app.redY,  app.radius, fill = 'red')
    drawLine(app.lineMin,app.thresholdY, app.lineMax, app.thresholdY)
    drawCircle(app.thresholdX, app.thresholdY,  app.radius, fill = 'black')
    drawRect(0,0, app.lineMax+50, 950, fill = None, border = "blue", borderWidth = 20)
    drawLine(app.lineMin,app.threshold2Y, app.lineMax, app.threshold2Y)
    drawCircle(app.threshold2X, app.threshold2Y,  app.radius, fill = 'yellow')
    drawRect(app.lineMin, app.optionsY, 120, 50, fill = 'black')
    drawLabel("Red-Green Transform", (app.lineMin)+(135)/2-7, app.optionsY+25, size=11, fill = "white")
    drawRect(app.lineMin+140, app.optionsY, 120, 50, fill = 'black')
    drawLabel("Blue-Yellow Transform", (app.lineMin+135)+(115)/2+6, app.optionsY+25, size=11, fill = "white")

    if app.saved:
        drawRect(1300, app.optionsY+30, 200, 50, fill = 'black')
        drawLabel("Your image is saved", 1410, app.optionsY+55, size=15, fill = "white")
    else:
        drawRect(1300, app.optionsY+30, 200, 50, fill = 'black')
        drawLabel("Click here to save image", 1400, app.optionsY+55, size=15, fill = "white")

    drawLabel("Use the sliders below ", app.center, 50, size=25)
    drawLabel("to adjust red, green,", app.center, 80, size=25)
    drawLabel("blue, the black slider for the", app.center, 110, size=25)
    drawLabel("border, and the yellow slider", app.center, 140, size=25)
    drawLabel("for the flood fill", app.center, 170, size=25)

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
            
            if(app.flooded and app.floodArr[i][j]):
                drawRect(x,y,rectWidth, rectHeight, fill = 'yellow')
            x += rectWidth
        y += rectHeight

# the following function checks which of the sliders are chosen and only moves them if they are chosen.
def transformedImageWithSliders_onMousePress(app, mouseX, mouseY):
    if distance(mouseX, app.blueX, mouseY, app.blueY)< app.radius:
        app.blueCircle = not app.blueCircle
        app.redCircle = False
        app.greenCircle = False
        app.threshold = False
        app.threshold2 = False
    elif distance(mouseX, app.greenX, mouseY, app.greenY)< app.radius:
        app.greenCircle = not app.greenCircle
        app.redCircle = False
        app.blueCircle = False
        app.threshold = False
        app.threshold2 = False
    elif distance(mouseX, app.redX, mouseY, app.redY)< app.radius:
        app.redCircle = not app.redCircle
        app.blueCircle = False
        app.greenCircle = False
        app.threshold = False
        app.threshold2 = False
    elif distance(mouseX, app.thresholdX, mouseY, app.thresholdY)<app.radius:
        app.threshold = not app.threshold
        app.redCircle = False
        app.blueCircle = False
        app.greenCircle = False
        app.threshold2 = False
    elif distance(mouseX, app.threshold2X, mouseY, app.threshold2Y)<app.radius:
        app.threshold2 = not app.threshold2
        app.threshold = False
        app.redCircle = False
        app.blueCircle = False
        app.greenCircle = False
    if mouseX>app.lineMin and mouseX<app.lineMin+120 and mouseY>app.optionsY and mouseY<app.optionsY+50:
        app.redGreen = not app.redGreen
        app.enhanced = enhanceForColorblindness(app)
    if mouseX>app.lineMin+140 and mouseX<app.lineMin+140+120 and mouseY>app.optionsY and mouseY<app.optionsY+50:
        app.blueYellow = not app.blueYellow
        app.enhanced = enhanceForColorblindness(app)

    if mouseX>1300 and mouseX<1500 and mouseY>app.optionsY+60 and mouseY<app.optionsY+110:
        outFile = "trasnformedImage"+app.expr
        saveRgbArrayAsPng(app.enhanced, app.border, app.floodArr, outFile)
        app.saved = True

    if mouseX > app.startX and mouseX<app.startX+len(app.enhanced)*10 and mouseY>app.startY and mouseY<app.startY+len(app.enhanced[0])*10:
        app.floodX = (mouseX-app.startX)//10
        app.floodY = (mouseY-app.startY)//10
        app.floodArr = floodFill(app, app.enhanced, app.floodX, app.floodY, 0)
        app.flooded = True


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
    if app.threshold:
        if mouseX>app.lineMax:
            app.thresholdX = app.lineMax
        elif mouseX<app.lineMin:
            app.thresholdX = app.lineMin
        else:
            app.thresholdX = mouseX
        app.changeThreshold = (app.thresholdX - app.center)
            
        #the following line of code ensures that the threshold is between 0 and 360 which are the min and max values that hue can reach.
        threshold = max(0, min(360, 30 + app.changeThreshold))
        app.border = findHueBorder(app.originalRgb, threshold)

    if app.threshold2 and app.flooded:
        if mouseX>app.lineMax:
            app.threshold2X = app.lineMax
        elif mouseX<app.lineMin:
            app.threshold2X = app.lineMin
        else:
            app.threshold2X = mouseX

        app.changeThreshold2 = (app.threshold2X - app.center)
        app.threshold2Value = max(0, app.changeThreshold2)
        app.floodArr = floodFill(app, app.enhanced, app.floodX, app.floodY, 0)


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

    for row in app.originalRgb:
        adjustedRow = []
        for r, g, b in row:
            h, s, v = rgbToHsv(r, g, b)
            
            # Adjust for red and green hues - addressing red-green colorblindness
            if ((0 <= h < 60) or (300 <= h < 360)) and app.redGreen:  # Red and magenta hues
                # Shift reds to blue (around 270)
                h = 270
            elif 120 <= h < 180 and app.redGreen:  # Green hues
                # Shift greens to yellow (around 90)
                h = 90

            #Adjust for blue and yellow hues - addressing blue-yellow colorblindness
            elif (240 <= h < 300) and app.blueYellow:
                #Shift blues to cyans (around 210)
                h = 210
            elif(60 <= h < 120) and app.blueYellow:
                h = 30

            newR, newG, newB = hsvToRgb(h, s, v)
            adjustedRow.append((newR, newG, newB))
        
        adjustedImage.append(adjustedRow)
    
    return adjustedImage


"""
The idea for the following recursive approach came from a conversation with my TP Mentor, Angie Chi (achi2), who shared that I could explore a flood fill algorithm to detect borders
I did some more research and brainstorming on ways to do border detection recursively and found the DFS algorithm, which is much like backtracking, but has no condition in which it terminates, because there is no condition under which it terminates.
This algorithm made sense in this use case, since there is no standard case in which the algorithm should terminate.
I used the following source to develop a better understanding: https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/ and https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/ 
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
    seen = [[False for i in range(cols)] for j in range(rows)]
    border = [[False for i in range(cols)] for j in range(rows)]

    if hueThreshold>350:
        hueThreshold = 350
     
    if hueThreshold<10:
        hueThreshold = 10
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  
    
    #the following code works because hue's wrap around in values back to 360, so rather than there being a diffence of 340 between 10 and 350, there is actually a difference of 20
    def isBorder(hue, newHue):
        diff = abs(hue - newHue)
        return min(diff, 360 - diff) > hueThreshold
    
    #the following function goes determines whether a startpoint is a border, and then goes down the tree to determine if the border continues. This is most efficient, because it is likely that one border pixel has other border pixels around it
    def recursive(row, col):
        seen[row][col] = True
        hue = hsvArray[row][col][0]
        (r,g,b) = rgbArray[row][col]
        
        borderPixel = False
        for nextR, nextC in directions:
            currR, currC = row + nextR, col + nextC
            if 0 <= currR < rows and 0 <= currC < cols and not seen[currR][currC]:
                newHue = hsvArray[currR][currC][0]
                #the following line ensures that there aren't any edges that are bordering white since this would already be clear to a colorblind person
                if r+g+b != 255*3 and isBorder(hue, newHue):
                    borderPixel = True
                    recursive(currR, currC)
        
        border[row][col] = borderPixel
    #the following loop goes through all the elements, but wil often not have to check because the recursive step above will determine large groups of border recursively
    for i in range(rows):
        for j in range(cols):
            if not seen[i][j]:
                recursive(i, j)
    
    return border

#please note that the following flood fill algorithm is experimentational and only works for certain images, which is why there is a combinate of potential methods
#this method was implemented based on ideas from Professor Austin Shick and Angie, my TP mentors as mentioned earlier.
#the function below simply uses recursion to go through all neighboring points from a defined starting point, and check if they are within a threshold that is defined by user 

def floodFill(app, image, col, row, count):

    rows, cols = len(image), len(image[0])
    originalColor = image[row][col]
    r,g,b = originalColor

    if originalColor == (255,255,255) or originalColor == (0,0,0):
        return [[False for i in range(cols)] for j in range(rows)]

    map = [[False for i in range(cols)] for j in range(rows)]
    
    def validPixels(r, c, count):
        if count < 700 and (0 <= r < rows and 0 <= c < cols and colorDistance(image[r][c],originalColor)<app.threshold2Value and not map[r][c] and image[r][c]!=(255,255,255) and image[r][c]!=(0,0,0)):
            map[r][c] = True
            validPixels(r - 1, c, count+1)  
            validPixels(r + 1, c, count+1)  
            validPixels(r, c - 1, count+1)  
            validPixels(r, c + 1, count+1) 
            validPixels(r - 1, c-1, count+1)  
            validPixels(r + 1, c+1, count+1)  
            validPixels(r+1, c - 1, count+1)  
            validPixels(r-1, c + 1, count+1)
    
    validPixels(row, col, count)

    return map

def colorDistance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def main():
    runAppWithScreens(initialScreen='start')
   
main()
