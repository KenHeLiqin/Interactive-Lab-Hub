import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime
import os
from datetime import datetime, timezone
import pytz

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

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

cwd = os.getcwd()

list_city = ['NY','LA','LDN','BJ']
current_city_index = 0
list_timezone = ['US']
current_timezone_index = 0
demo_NY_hour = 8
demo_hour = demo_NY_hour
demo_hour_delayer = 0

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py

    # est = pytz.timezone('US/Eastern')
    # est_now = datetime.now(est)
    # strDate = est_now.strftime('%A %m %b %Y')
    # strTime = est_now.strftime('%H: %M: %S')
    # strhour = est_now.strftime('%H')
    # Hour = int(strhour)
    # strmin = est_now.strftime('%M')
    # Min = int(strmin)
    #
    # strsec = est_now.strftime('%S')
    # Sec = int(strsec)

    current_time = time.strftime("%m/%d/%Y %H:%M:%S")
    date_str, time_str = current_time.split(" ")
    hour, min, sec = time_str.split(":")

    # change 24 hours to 12 hours
    # if int(hour) > 12:
    #     hour_12 = int(hour) - 12
    #     light_source_pos = hour * 20
    #     hour_12 = str(hour)

    # # detect day or night
    # if int(hour) > 7 and int(hour) < 19:
    #     day = True
    # else:
    #     day = False


    # set city index
    if buttonA.value and (not buttonB.value): # button B pressed
        current_city_index += 1
        if current_city_index == 4:
            current_city_index = 0
    elif (not buttonA.value) and buttonB.value: # button A pressed
        current_city_index -= 1
        if current_city_index == -4:
            current_city_index = 0

    # set timezone index
    # if list_city[current_city_index] == 'NY':
    #
    # elif list_city[current_city_index] == 'LA':
    #
    # elif list_city[current_city_index] == 'LDN':
    #
    # elif list_city[current_city_index] == 'BJ':


    # for demo: day or night
    if int(demo_hour) > 7 and int(demo_hour) < 20:
        demo_day = True
    else:
        demo_day = False

    # for demo: hour to str
    demo_hour_str = str(demo_hour)

    # load sun or moon pic

    if demo_day:
        image = Image.open(cwd + "/pic/" + demo_hour_str + ".jpg")
    else:
        image = Image.open(cwd + "/pic/" + demo_hour_str + ".png")

    image = image.convert('RGBA')
    image = image.resize((45, 45), Image.BICUBIC)

    # draw = ImageDraw.Draw(image)
    # draw.text((70, 110), time_str, font=font, fill="#FFFFFF")

    demo_pos = (demo_hour - 8) * 16

    # paste day or night background for city.

    if demo_day:
        background = Image.open(cwd + "/pic/"+ list_city[current_city_index] +".jpg")
    else:
        background = Image.open(cwd + "/pic/"+ list_city[current_city_index] +"_night.jpg")


    background = background.resize((240, 135), Image.BICUBIC)

    # paste moon or sun to the background, and set its position

    sun_pos_y = int(((demo_pos - 90)**2)/250)

    if demo_day: # change demo_day to day
        background.paste(image, (demo_pos, sun_pos_y), image) # change test_pos to light_source_pos.
    else:
        background.paste(image, (180 ,10), image)

    # for demo, changing of hours
    demo_hour_delayer += 1
    if demo_hour_delayer % 10 == 0:
        demo_NY_hour += 1
        if demo_NY_hour == 25:
            demo_NY_hour = 1

    # Display image.
    disp.image(background, rotation)
    time.sleep(0.1)

