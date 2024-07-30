#!pip install opencv.python
#!pip install pytesseract

import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract
from cv2 import cvtColor

pytesseract.pytesseract.tesseract_cmd = "D:/tesseract/tesseract.exe"

#internal player string
def player_type(player):
    player_string = ""
    if player.pos == "SP":
        player_string  += "1"
    elif player.pos ==  "CP" or player.pos == "RP":
        player_string += "0"
    elif player.pos == "C":
        player_string += "2"
    elif player.pos == "1B":
        player_string += "3"
    elif player.pos == "2B":
        player_string += "4"
    elif player.pos == "Third Base" or "3b":
        player_string += "5"
    elif player.pos == "Short Stop" or "ss":
        player_string += "6"
    elif player.pos == "LF":
        player_string += "7"
    elif player.pos == "CF":
        player_string += "8"
    elif player.pos == "RF":
        player_string += "9"
    
    return player_string

#is this player a two way player?
def two_way_player(player):
    pitch_test = 0
    hit_test = 0
    if player.pos == "Starting Pitcher" :
        pitch_test += 1
    elif player.pos == "CP":
        pitch_test += 1
    elif player.pos == "RP":
        pitch_test += 1
    else:
        hit_test += 1

    if hit_test != 1:
        if type(player.secondary) == type("hello"):
            if player.secondary in position_players:
                hit_test += 1
        else:
            for i in range(len(player.secondary)):
                if player.secondary[i] in position_players:
                    hit_test +=1

    if player.pos in position_players:
        if player.sec == "SP" :
            pitch_test += 1
        elif player.sec == "CP":
            pitch_test += 1
        elif player.sec == "RP":
            pitch_test += 1

    if pitch_test > 0 and hit_test > 0:
        return True
    else:
        return False

#create a player
class player:
    def __init__(self, Name, Pos, Series):
        self.name=Name
        self.pos=Pos
        self.series=Series
        self.secondary = []
        self.stats = []
        self.playertype=-1
        self.twowayplayer = False

    def __iter__(self):
        return self

    def __str__(self):
        return str(str(self.name) +"\n" + str(self.pos) + "\n" + str(self.series))

    def setName(self, newname):
        self.name = newname
        return

    def setPos(self, newPos):
        self.pos = newPos
        return

    def set2nd(self, new2):
        if "," in new2:
            self.secondary = new2.split(", ")
        else:
            self.secondary = new2
        return

    def print2nd(self):
        print(self.secondary)

    def addstats(self, stats):
        self.stats = stats

    
    def setSeries(self, newseries):
        self.series = newseries
        return

    def update_player_type(self):
        self.playertype=  int(player_type(self))

    def update_two_way_player(self):
        self.twowayplayer = two_way_player(self)
           

hitter_stats = ['CON R', 'CON L', 'POW R', 'POW L', 'VIS','DISC', 'CLT', 'BUNT', 'DBUNT', 'DUR', 'FLD', 'ARM', 'ACC', 'REAC', 'SPD', 'STEAL', 'BR AGG']

def getnewimage():
    im1 = pyautogui.screenshot('sample.png')

def readpic(pic, h1, h2, w1, w2):
    #pic = cv2.Lab(pic,cv2.CV_64F,0,1,ksize=5)
    cropped_image = pic[h1:h2, w1:w2]
    
    # Save the cropped image
    cv2.imwrite("playerinfo.jpg", cropped_image)
    
    # Preprocessing the image starts
    # Convert the image to gray scale
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Creating a copy of image
    playerinfopic = cropped_image.copy()
    # A text file is created and flushed
    file = open("playerinfo.txt", "w+")
    file.write("")
    file.close()

    text = ""
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(playerinfopic, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cropping the text block for giving input to OCR
        cropped = playerinfopic[y:y + h, x:x + w]
        # Open the file in append mode
        file = open("playerinfo.txt", "a")
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped).strip()
        # Appending the text into file
        file.write(text)
        file.close
        #print(cropped)

    file = open("playerinfo.txt", "r")
    text = file.readline().strip()
    #print(text)
    return text

def gatherstats(fullpic, log):
    statlist = []
    totalflag = True
    logtest = []
    for i in range(17):
        #print(i+1)
        increase = i * 100
        #print(increase)
        w1 = 120 + increase
        w2 = 180 + increase
        #print(w1, w2)
        stat = readpic(fullpic, 610, 645, w1, w2)
        
        flag = True
        try:
            int(stat)
        except ValueError:
            flag = False
            
        if flag == False:
            totalflag = False
            log.append(i)
            logtest.append(i)
            #savestring = ("playerinfo" + str(i)+".jpg")
            #temp = cv2.imwrite(savestring, fullpic[420:460, w1:w2])
            #stat = readpic(fullpic, 0, 40, 0, 65)
        if flag:
            stat = int(stat)
        #print(stat)
        statlist.append(stat)
    if totalflag:
        return statlist
    elif log == logtest:
        logtest = []
        return gatherstats(fullpic, log)
    else:
        x = len(log)//2
        for i in range(x):
            statlist[log[i]] = int(input(str("Enter the player's " + str(hitter_stats[log[i]]) +  " stat:")))
    return statlist

def createplayer(img):
    name = readpic(img, 90, 140, 430, 1250)
    #print(name)
    position = readpic(img, 140, 180, 430, 700)
    #print(position)
    series = readpic(img, 175, 210, 430, 1000)
    #print(series)
    tempplayer = player(name, position, series)
    print(tempplayer)
    secondary = readpic(img, 230, 272, 950, 1375)
    tempplayer.set2nd(secondary)
    log = []
    playerstats = gatherstats(img, log)
    #blankplayer = (name, "None", "None")
    if playerstats[0] == "-1":
        getnewimage()
        retry = cv2.imread("C:/Users/Gilahead/Desktop/Other/MLBtheMets/sample.png")
        playerstats = gatherstats(retry, log)

    x = len(log)//2
    if playerstats == log[:x]:
        for i in range(x):
            pass
        return log[:x]
    else:
        tempplayer.addstats(playerstats)
        return tempplayer

#this_pic = cv2.imread('C:/Users/Gilahead/Desktop/Other/MLBtheMets/Images/david_wright_kaiju.png')
#this_pic = cv2.imread('C:/Users/Gilahead/Desktop/Other/MLBtheMets/Images/martin_dihigo_hitter.png')

def createhitter():
    getnewimage()
    this_player = createplayer(cv2.imread("C:/Users/Gilahead/Desktop/Other/MLBtheMets/sample.png"))
    testinglist = []
    if type(this_player) == type(testinglist):
        print(this_player)
        #getstats(this_player)
    else:
        print(this_player.stats)
    
   
createhitter()

#this_player.update_player_type()
#this_player.update_two_way_player()
