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
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

'''
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
'''
nums = ["1","2","3","4"]

screenColor = color565(125, 255, 255)

while True:
    num = choice(nums)
    print("Num ",  num)
    y = top
    txt1 = "Great"
    txt2 = "Fail"
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, y), num, font=font, fill="#FFFFFF")
    y += font.getsize(txt1)[1]

    t = 0.5
    success = False
    while t > 0:
        if mpr121[int(num) - 1].value:
                print(f"touched!")
                draw.text((x, y), txt1, font=font, fill="#FFFF00")
                success = True
                break
        time.sleep(0.1)
        t -= 0.1

    if not success:
        draw.text((x, y), txt2, font=font, fill="#FFFF00")

    time.sleep(0.5)

    y = top

    

    # Display image.
    disp.image(image, rotation)
    draw.rectangle((0, font.getsize(txt1)[1], width, height), outline=0, fill=0)
    time.sleep(0.5)