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
        self.words = self.mytext.split() # Split by whitespace
        for word in self.words:
            if len(self.line.split()) == 0:
                self.line = word
            else:
                self.line = "{} {}".format(self.line, word)
            self.line_width, self.line_height = self.d.textsize(self.line, font = self.font)
            if self.line_width > self.max_width:
                # This block was saving the width of the line including the word which pushed it over the limit
                # Have corrected it to re-calculate the line width after removing the word
                # But it's v hacky – will come back to it when I have more time
                last_word = self.line.rsplit(" ", 1)[-1] # Save last word
                self.line = self.line.rsplit(" ", 1)[0] # Strip it from line
                self.line_width, self.line_height = self.d.textsize(self.line, font = self.font) # Recalculate line width
                self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line})
                self.line = last_word # Replace line with last word
        self.line_width, self.line_height = self.d.textsize(self.line, font = self.font) # Recalculate line width
        self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line}) # Catch the last line

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
            self.d.text((x, y), self.line["string"], font = self.font, fill = (255,255,255,128)) # To justify right, would set x to original_image.size[0] - line["width"]

        self.out = Image.alpha_composite(self.original_image, self.text_placeholder)
        self.out.save(os.path.join("photos", self.myimage+".edit.jpg"))
