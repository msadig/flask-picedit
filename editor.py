#!/usr/bin/python
# -*- coding: utf-8 -*- 
import PIL
from PIL import ImageFont, Image, ImageDraw
import textwrap

'''
 - http://www.xappsoftware.com/wordpress/2013/04/25/how-to-add-a-text-to-a-picture-using-python/
 - http://stackoverflow.com/a/7698300/968751
'''

My_TEXT = "Dünyanın günəş yox öz dalı ətrafında fızrlandığını fikirləşən bütün qadınların qabaqdan gələn bayram gözünə girsin.. elə kişilərin də!"


# Loading Fonts….
# Note the following line works on Ubuntu 12.04
# On other operating systems you should set the correct path
# To the font you want to use.
font = ImageFont.truetype("fonts/centry.ttf", 36, encoding='unic')
imagePath = "template.jpg"
imgFile = Image.open(imagePath)
draw = ImageDraw.Draw(imgFile)
TEXT = My_TEXT.decode('utf-8')
# draw.text((20, 145), TEXT, (0,0,0), font=font)
# draw = ImageDraw.Draw(im1)


# multi line
from_top, h = 100, 30
lines = textwrap.wrap(TEXT, width = 35)
y_text = h
for line in lines:
    width, height = font.getsize(line)
    draw.text((20, y_text + from_top), line, (0,0,0), font = font)
    y_text += (height + 22)

# Save the image with a new name
imgFile.save("result.jpg")
print(len(TEXT))


