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
x, y, font_size = 10, 10, 36
text_placeholder = Image.new("RGBA", original_image.size, (255,255,255,0))
font = ImageFont.truetype("OpenSans-Bold.ttf", font_size)
d = ImageDraw.Draw(text_placeholder)
size = d.textsize(text_list[0], font = font)
if size[0] > original_image.size[0]:
    print("Text too long, needs to be wrapped")
d.text((x,y), text_list[0], font = font, fill = (255,255,255,128))
out = Image.alpha_composite(original_image, text_placeholder)
out.save(image_list[0]+".jpg") # Overwrite original, could change filename
