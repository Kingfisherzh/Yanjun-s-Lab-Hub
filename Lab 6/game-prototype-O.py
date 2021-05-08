import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from adafruit_rgb_display.rgb import color565
import webcolors
from random import choice

import time
import board
import busio

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000
# Setup SPI bus using hardware SPI:
spi = board.SPI()
# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
rotation = 90
image = Image.new("RGBA", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# # Draw a white filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))

# Always paste later image to primal image
background = Image.open("move-img/background.png").resize((height, height))
image.paste(background, (0,0),background)

disp.image(image, rotation)


font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


###################################################
###################################################
# Sender and Reader
import paho.mqtt.client as mqtt
import uuid

# Global variable, current content
content = "111"

topic = 'IDD/tic-tac-toc'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
    if msg.topic == topic:
        global content
        content = msg.payload.decode('UTF-8')
        print("on_message: ", content)

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()
###################################################
###################################################
def printBoard(move, player, image, disp, rotation):
    # Draw board with player and move
    newImg = Image.open("move-img/{}{}.png".format(move, player)).resize((height, height))
    image.paste(newImg, (0,0),newImg)
    disp.image(image, rotation)


def printText(image, draw, txt):
    y = 0
    draw.rectangle((int(width/2)+20, 0, width, height), outline=0, fill="#FFFFFF")
    words = txt.split()
    for i in range(len(words)):
        draw.text((int(width/2)+20, y), words[i], font=font, fill="#000000")
        disp.image(image, rotation)
        y += 32


def check(turn, count, theBoard):
    print(count)
    if count >= 5:
        if theBoard['7'] == theBoard['8'] == theBoard['9'] != '':
            txt = turn + " won."                 
            printText(image, draw, txt)               
        elif theBoard['4'] == theBoard['5'] == theBoard['6'] != '':   
            txt = turn + " won."                 
            printText(image, draw, txt) 
        elif theBoard['1'] == theBoard['2'] == theBoard['3'] != '': 
            txt = turn + " won."                 
            printText(image, draw, txt) 
        elif theBoard['1'] == theBoard['4'] == theBoard['7'] != '': 
            txt = turn + " won."                 
            printText(image, draw, txt) 
        elif theBoard['2'] == theBoard['5'] == theBoard['8'] != '':
            txt = turn + " won."                 
            printText(image, draw, txt) 
        elif theBoard['3'] == theBoard['6'] == theBoard['9'] != '':   
            txt = turn + " won."                 
            printText(image, draw, txt) 
        elif theBoard['7'] == theBoard['5'] == theBoard['3'] != '':      
            txt = turn + " won."                 
            printText(image, draw, txt) 
        elif theBoard['1'] == theBoard['5'] == theBoard['9'] != '':     
            txt = turn + " won."                 
            printText(image, draw, txt) 

    # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
    if count == 9:
        txt = "It's a Tie!!"             
        printText(image, draw, txt)              
        return True          

###################################################
###################################################


theBoard = {'1': '' , '2': '' , '3': '' ,
            '4': '' , '5': '' , '6': '' ,
            '7': '' , '8': '' , '9': '' }

turn = 'O'
enemy = 'X'
count = 0
end = False
touched = False

"""
# Detect enemy
while content != enemy:
    # Send a signal to broker
    client.publish(topic, turn)
    time.sleep(0.5)
"""

# Game start
while content != enemy + 'win':
    txt = "Wait your oppo"
    printText(image, draw, txt)
    # Enemy's turn, detect enemy signal
    while True:
        if len(content) == 2 and content[1] == enemy:
            move, player = content[0], content[1]
            if player == enemy:
                printBoard(move, player, image, disp, rotation)
                theBoard[move] = player
                count += 1
                break
    
    # Now we will check if player X or O has won,for every move after 5 moves. 
    end = check(turn, count, theBoard)
    if end:           
        break

    touched = False

    txt = "It's your turn," + turn
    printText(image, draw, txt)

    # Your turn
    while not touched:
        # Detect which pin is touched
        for i in range(1,10):
            if mpr121[i].value:
                move = i
                # If blank
                if theBoard[str(move)] == '':
                
                    theBoard[str(move)] = turn
                    count += 1
                    printBoard(move, turn, image, disp, rotation)
                    touched = True
                # If not blank
                else:
                    txt = "Not allowed. Try again."
                    printText(image, draw, txt)
                    continue   

    # Send a signal, e.g. 1X
    client.publish(topic, str(move) + turn)
    content = str(move) + turn

    # Clear text
    txt = "Wait your oppo"
    printText(image, draw, txt)

    # Now we will check if player X or O has won,for every move after 5 moves. 
    end = check(turn, count, theBoard)
    if end:           
        break


    


