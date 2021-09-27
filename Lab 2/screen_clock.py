import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime
import os

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331

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

height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# Draw some shapes.
# # First define some constants to allow easy resizing of shapes.
# padding = -2
# top = padding
# bottom = height - padding
# # Move left to right keeping track of the current x position for drawing shapes.
# x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

cwd = os.getcwd()

# while True:

draw.rectangle((0, 0, width, height), outline=0, fill=0)
image = Image.open(cwd + "/sun_pic/" + "1" +".jpg")

# Scale the image to the smaller screen dimension
image_ratio = image.width / image.height
screen_ratio = width / height

# if screen_ratio < image_ratio:
#     scaled_width = image.width * height // image.height
#     scaled_height = height
# else:
#     scaled_width = width
#     scaled_height = image.height * width // image.width

scaled_width = 10
scaled_height = 10
image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image = image.crop((x, y, x + width, y + height))

# Display image.
disp.image(image, rotation)

# # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
# cs_pin = digitalio.DigitalInOut(board.CE0)
# dc_pin = digitalio.DigitalInOut(board.D25)
# reset_pin = None
#
# # Config for display baudrate (default max is 24mhz):
# BAUDRATE = 64000000
#
# # Setup SPI bus using hardware SPI:
# spi = board.SPI()
#
# # Create the ST7789 display:
# disp = st7789.ST7789(
#     spi,
#     cs=cs_pin,
#     dc=dc_pin,
#     rst=reset_pin,
#     baudrate=BAUDRATE,
#     width=135,
#     height=240,
#     x_offset=53,
#     y_offset=40,
# )
#
# # Create blank image for drawing.
# # Make sure to create image with mode 'RGB' for full color.
# height = disp.width  # we swap height/width to rotate it to landscape!
# width = disp.height
# image = Image.new("RGB", (width, height))
# rotation = 90
#
# buttonA = digitalio.DigitalInOut(board.D23)
# buttonB = digitalio.DigitalInOut(board.D24)
# buttonA.switch_to_input()
# buttonB.switch_to_input()
#
# # Get drawing object to draw on image.
# draw = ImageDraw.Draw(image)
#
# # Draw a black filled box to clear the image.
# draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image, rotation)
#
# # Draw some shapes.
# # First define some constants to allow easy resizing of shapes.
# padding = -2
# top = padding
# bottom = height - padding
# # Move left to right keeping track of the current x position for drawing shapes.
# x = 0
#
# # Alternatively load a TTF font.  Make sure the .ttf font file is in the
# # same directory as the python script!
# # Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
#
# # Turn on the backlight
# backlight = digitalio.DigitalInOut(board.D22)
# backlight.switch_to_output()
# backlight.value = True
#
# cwd = os.getcwd()
#
# current_page = 1
#
# while True:
#     # Draw a black filled box to clear the image.
#     draw.rectangle((0, 0, width, height), outline=0, fill=0)
#
#     #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py
#
#     current_time = time.strftime("%m/%d/%Y %H:%M:%S")
#     date_str, time_str = current_time.split(" ")
#     hour, min, sec = time_str.split(":")
#
#     if int(hour) > 12:
#         hour = int(hour) - 12
#         hour = str(hour)
#
#     if current_page == 1:
#         # image = Image.open(cwd + "/sun_pic/" + hour + ".jpg") # change 1 to hour
#         image = Image.open(cwd + "/red.jpg") # change 1 to hour
#         image = image.convert('RGBA')
#         # draw = ImageDraw.Draw(image)
#         # draw.text((70, 110), time_str, font=font, fill="#FFFFFF")
#
#
#     # Scale the image to the smaller screen dimension
#
#     image_ratio = image.width / image.height
#     screen_ratio = width / height
#     if screen_ratio < image_ratio:
#         scaled_width = image.width * height // image.height
#         scaled_height = height
#     else:
#         scaled_width = width
#         scaled_height = image.height * width // image.width
#     image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
#
#     # Crop and center the image
#     x = scaled_width // 2 - width // 2
#     y = scaled_height // 2 - height // 2
#     image = image.crop((x, y, x + width, y + height))
#
#     # Display image.
#     disp.image(image, rotation)
#     time.sleep(1)

