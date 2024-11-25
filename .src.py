from cmu_graphics import *

def onAppStart(app):
    #all images and data from colormax.org

    app.imageArr = [
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image1.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image2.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image3.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image4.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image5.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image6.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image7.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image8.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image9.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image10.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image11.jpg',
        'https://cdn-beaai.nitrocdn.com/DsHNrqyidSdrnEUwxpnDFmLjguAlTfrt/assets/images/optimized/rev-f0a997b/colormax.org/wp-content/uploads/2015/08/colorblind-test-image12.jpg'
    ]
    app.correctAnswers = [7, 6, 26,15,6,73,5,16,45,12,29,8]
    app.alternateAnswers = [
    (0,), (0,), (6, 2), (17,), (0,), (0,), (0,), (0,), (0,), (0,), (70,), (3, 0)
    ]
    app.tempMeaning = [
    ("Colorblind",), ("Colorblind",), ("red-green",), ("Colorblind",), 
    ("Colorblind",), ("Colorblind",), ("Colorblind",), ("Colorblind",), 
    ("Colorblind",), ("red-green",), ("red-green",)
    ]
    app.answerMeaning = [
    (None,), (None,), ("red", "green"), ("red-green",), (None,), (None,), 
    (None,), (None,), (None,), (None,), ("red-green",), ("red-green",)
    ]

    app.d = {"colorblind": 0, "red-green":0}
    app.expr = ""
    app.countAnswered = 1
    app.guesses = []

def redrawAll(app):
    cols = 4
    rows = 3
    imageWidth = 150
    imageHeight = 150
    spaceX = 120
    spaceY = 160

    startX = 35
    startY = 10

    for i in range(len(app.imageArr)):
        row = i // cols  
        col = i % cols   

        x = startX + col * (imageWidth + spaceX)
        y = startY + row * (imageHeight + spaceY)

        drawImage(app.imageArr[i], x, y)
        curr = str(i+1)
        drawLabel(curr, x,y)
    if app.countAnswered <= 12:
        drawLabel(f"Type in the number you see in circle {app.countAnswered}", startX + spaceX*10, startY)
        drawLabel(str(app.expr),startX + spaceX*10, startY+30)
        

def onKeyPress(app, key):
    if(key.isdigit()):
        app.expr+=key
    if(key == "enter" and app.countAnswered<=12):
        app.guesses.append(app.expr)
        app.expr = ""
        app.countAnswered+=1
    elif(key=='backspace' and app.expr!=""):
        app.expr = app.expr[0:len(app.expr)-1]

def evaluatedExpr(expr):
    firstNum = int(expr[0:expr.find("+")])
    secondNum = int(expr[expr.find("+")+1:len(expr)])
    return expr + "=" + str(firstNum+secondNum)

def checkResults(app):
    for i in range (len(app.guesses)):
        if app.guesses[i] == app.correctAnswers[i]:
            continue
        else:
            for j in range(len(app.alternateAnswer[i])):
                if app.guesses[i] == app.alternateAnswer[i][j]:
                    app.d[app.tempMeaning[i][0]] = app.d.get(app.tempMeaning[i][0],0)+1
    return app.d["Colorblind"], app.d["red-green"]
def main():
    runApp()
    colorBlindCount, redGreenCount = checkResults()
    print(colorBlindCount, redGreenCount)

main()
