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

topic = 'IDD/4-Connect'

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
client.connect('farlab.infosci.cornell.edu', port=8883)

client.loop_start()


###################################################

def printText(image, draw, txt):
	y = 0
	draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")
	words = txt.split()
	for i in range(len(words)):
		draw.text((10, y), words[i], font=font, fill="#000000")
		disp.image(image, rotation)
		y += 32

###################################################

import numpy as np
import sys
import math

ROW_COUNT = 5
COLUMN_COUNT = 6

def create_board():
	board = [["_" for i in range(ROW_COUNT)] for j in range(COLUMN_COUNT)]
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_dropped(mpr121, col):
	return mpr121[col]

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == "_"

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == "_":
			return r

def print_board(board):
	for i in range(ROW_COUNT):
		print(board[i] + "\n")

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True



board = create_board()
game_over = False
mine = "X"
oppo = "O"
turn = mine

while not game_over:
	
	touched = False
	printText(image, draw, "It's your turn," + turn)

	# Your turn
	if turn == mine:
		while not touched:
			# Detect which pin is touched
			for i in range(COLUMN_COUNT):
				if mpr121[i].value:
					col = i

			    # Detect if valid
			    if is_valid_location(board, col):
				    row = get_next_open_row(board, col)
				    drop_piece(board, row, col, mine)
				    touched = True

				    # Detect if won
				    if winning_move(board, mine):

					    # Show won
					    printText(image, draw, "You won")

					    # Send a won signal, 12XW
					    content = str(row) + str(col) + turn + "W"
					    client.publish(topic, content)
					    game_over = True

				    else:
					    # Send a normal signal, e.g. 12X
					    content = str(row) + str(col) + turn
					    client.publish(topic, content)
				    
				    break
                
			turn = oppo

	# Oppo turn
	elif turn == oppo:				
		while True:

			# Detect if oppo dropped a piece
			if content[2] == oppo:

				row, col = content[0], content[1] 
				drop_piece(board, row, col, oppo)

				# Place oppo move
				while not is_dropped(mpr121, col):
					printText(image, draw, "Place at col {}".format(col))

				printText(image, draw, "Done")
				time.sleep(1.0)	

				# Detect if oppo won
				if len(content) == 4 and content[3] == "W":
					game_over = True
					printText(image, draw, "Oppo won")
				
				break
				
		turn = mine

	print_board(board)