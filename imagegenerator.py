# Module containing the Imagegenerator class which overlays text on images.
# It takes a list of images, a list of text, and a list of user genereated
# text locations as arguments.

import os, glob, random
from PIL import Image, ImageDraw, ImageFont # Install Pillow, not PIL

class Imagegenerator():
    def __init__(self, data_list, user_preferences):
        self.overlayimage_list(data_list, user_preferences)

    def overlayimage_list(self, data_list, user_preferences):
        self.image_list, self.text_list = data_list
        self.user_preferences = user_preferences
        self.font_file_list = glob.glob(os.path.join("fonts", "*.ttf"))
        random.shuffle(self.font_file_list)

        for i in range(len(self.text_list)):
            if user_preferences[1].rstrip() == "random":
                self.font_file = self.font_file_list[i % len(self.font_file_list)]
            else:
                self.font_file = os.path.join("fonts", user_preferences[1].rstrip())
            self.overlayimage(self.image_list[i], self.text_list[i])
     
    def line_to_paragraph(self):
        self.font_size = int(self.user_preferences[0])
        self.original_image = Image.open(os.path.join("photos", self.myimage + ".jpg")).convert("RGBA")
        self.x, self.y, self.font_size, self.max_width = 10, 10, self.font_size, self.original_image.size[0] - 20
        self.text_placeholder = Image.new("RGBA", self.original_image.size, (255,255,255,0))
        self.font = ImageFont.truetype(self.font_file, self.font_size)
        self.d = ImageDraw.Draw(self.text_placeholder)
        self.line = ""
        self.lines = []
        self.words = self.mytext.split()
        # NB self.word, self.line, self.total_width, self.word_width & self.word_height are all local & don't need to be attributes
        for self.word in self.words:
            if len(self.line) > 0: # If there's already a word in line...
                self.word_width, self.word_height = self.d.textsize(" " + self.word, font = self.font) # Current word's width
                self.line_width, self.line_height = self.d.textsize(self.line, font = self.font) # Current line's width
                self.total_width = self.line_width + self.word_width # Total width
                if self.total_width > self.max_width: # If total width too wide...
                    self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line}) # Store the line in self.lines
                    self.line = self.word # And form new line with current word
                else: # If total width not too wide...
                    self.line += " " + self.word # Append current word
            else: # If line is empty...
                self.line = self.word # Start it with the current word
        self.line_width, self.line_height = self.d.textsize(self.line, font = self.font) # Get last line's width
        self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line}) # Append last line to lines

    def overlayimage(self, image, text):
        self.myimage = image
        self.mytext = text
        #self.font_size = user_preferences["font_size"]
        self.line_to_paragraph()
        for i, self.line in enumerate(self.lines):
            if self.user_preferences[2] == "Left":
                x = self.x
                y = self.y + (i * self.lines[i-1]["height"])
            elif self.user_preferences[2] == "Right":
                x = self.max_width - self.line["width"]
                y = self.y + (i * self.lines[i-1]["height"])
            elif self.user_preferences[2] == "Centre":
                x = (self.max_width - self.line["width"]) / 2
                y = self.y + (i * self.lines[i-1]["height"])
            else:
                x = self.x
                y = self.y + (i * self.lines[i-1]["height"])
            self.d.text((x, y), self.line["string"], font = self.font, fill = (255,255,255,128)) # To justify right, would set x to original_image.size[0] - line["width"]

        self.out = Image.alpha_composite(self.original_image, self.text_placeholder)
        self.out.save(os.path.join("photos", self.myimage+".edit.jpg"))
