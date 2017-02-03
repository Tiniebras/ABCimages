# ABC text overlay program
# Imports images from flickr and overlays
# text from a separate source.

#Flicker image loading module - returns
#a list of images and a list of text
import datagrabber
from PIL import Image, ImageDraw, ImageFont # Install Pillow, not PIL

#User input module to set text location
#preferences
#import userpreferences

#Image generating module
#import imagegenerator

#Main 
mydatagrabber = datagrabber.Datagrabber("flickr")
image_list, text_list = mydatagrabber.getdata_lists()
 
#mypreferences = userpreferences.Userpreferences(data_list)
#user_preferences = myprerfences.getpreferences()

#myimages = imagegenerator.Imagegenerator(data_list,user_preferences)

# What if image_list and text_list are different lengths?

original_image = Image.open(image_list[0]+".jpg").convert("RGBA")
x, y, font_size, max_width = 10, 10, 24, original_image.size[0] - 20
text_placeholder = Image.new("RGBA", original_image.size, (255,255,255,0))
font = ImageFont.truetype("OpenSans-Bold.ttf", font_size)
d = ImageDraw.Draw(text_placeholder)

# Should probably be a method... #
line = ""
lines = []
words = text_list[0].split() # Split by whitespace
for word in words:
    if len(line.split()) == 0:
        line = word
    else:
        line = "{} {}".format(line, word)
    line_width, line_height = d.textsize(line, font = font)
    if line_width > max_width:
        last_word = line.rsplit(" ", 1)[-1]
        lines.append({"width": line_width, "height": line_height, "string": line.rsplit(" ", 1)[0]})
        line = last_word
lines.append({"width": line_width, "height": line_height, "string": line}) # Catch the last line
# ...end method (would return lines dict) #

for i, line in enumerate(lines):
    d.text((x, y + (i * line["height"])), line["string"], font = font, fill = (255,255,255,128)) # To justify right, would set x to original_image.size[0] - line["width"]

out = Image.alpha_composite(original_image, text_placeholder)
out.save(image_list[0]+".edit.jpg")
