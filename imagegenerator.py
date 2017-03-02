# Module containing the Imagegenerator class which overlays text on images.
# It takes a list of images, a list of text, and a list of user genereated
# text locations as arguments.

import os, glob, random, datagrabber
from PIL import Image, ImageDraw, ImageFont # Install Pillow, not PIL

class Imagegenerator():
    def __init__(self, data_list, user_preferences):
        self.overlayimage_list(data_list, user_preferences)

    def overlayimage_list(self, data_list, user_preferences):
        #self.image_list, self.text_list = data_list
        #self.image_list, self.text_list = data_list.getdata_lists()
             
        #self.user_preferences = user_preferences
        self.user_preferences = user_preferences.getuserpreferences()
        
        self.font_file_list = glob.glob(os.path.join("fonts", "*.ttf"))
        random.shuffle(self.font_file_list)

        #for i in range(len(self.text_list)):
        for i in range(data_list.gettextlen()):
            if self.user_preferences[1].rstrip() == "random":
                self.font_file = self.font_file_list[i % len(self.font_file_list)]
            else:
                #self.font_file = os.path.join("fonts", self.user_preferences[1].rstrip())
                self.font_file = os.path.join("fonts", user_preferences.getfontname().rstrip())
            #self.overlayimage(self.image_list[i], self.text_list[i])
            #self.overlayimage(self.image_list[i], data_list.gettext(i))
            self.overlayimage(data_list.getimage(i), data_list.gettext(i), user_preferences)
   
    def overlayimage(self, image, text, user_preferences):
        self._line_to_paragraph(image, text, user_preferences)
        self._applytext(image, text, user_preferences)
            
    def _line_to_paragraph(self, image, text, user_preferences):
        self.font_size = int(self.user_preferences[0])
        self.original_image = Image.open(os.path.join("photos", image + ".jpg")).convert("RGBA")
        self.x, self.y, self.font_size, self.max_width = 10, 10, self.font_size, self.original_image.size[0] - 20
        self.text_placeholder = Image.new("RGBA", self.original_image.size, (255,255,255,0))
        self.font = ImageFont.truetype(self.font_file, self.font_size)
        self.d = ImageDraw.Draw(self.text_placeholder)
        self.multiline = ""
        line = ""
        words = text.split()
        for word in words:
            if len(line) == 0: # If line is empty...
                line = word # Start it with the current word
            else: # If there's already a word in line...
                word_width, word_height = self.d.textsize(" " + word, font = self.font, spacing = 0) # Current word's width
                line_width, line_height = self.d.textsize(line, font = self.font, spacing = 0) # Current line's width
                if (line_width + word_width) > self.max_width: # If total width too wide...
                    self.multiline += line + "\n" # Push line onto multiline and append \n
                    line = word # And form new line with current word
                else: # If total width not too wide...
                    line += " " + word # Append current word
        self.multiline += line # Append remaining line fragments

    #def overlayimage(self, image, text, user_preferences):
    def _applytext(self, image, text, user_preferences):
        #self.myimage = image
        #self.mytext = text
        #self.font_size = user_preferences["font_size"]
        #self.line_to_paragraph(image, text, user_preferences)
        x, y = self.x, self.y
        if user_preferences.gethorizontal() == "Left":
            self.d.multiline_text((x, y), self.multiline, font = self.font, fill = (255,255,255,128), align = "left")
        elif user_preferences.gethorizontal() == "Centre":
            self.d.multiline_text((x, y), self.multiline, font = self.font, fill = (255,255,255,128), align = "center")
        elif user_preferences.gethorizontal() == "Right":
            self.d.multiline_text((x, y), self.multiline, font = self.font, fill = (255,255,255,128), align = "right")
        else:
            self.d.multiline_text((x, y), self.multiline, font = self.font, fill = (255,255,255,128), align = "left")
        self.out = Image.alpha_composite(self.original_image, self.text_placeholder)
        self.out.save(os.path.join("photos", image+".edit.jpg"))
