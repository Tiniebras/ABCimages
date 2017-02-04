# Module containing the Imagegenerator class which overlays text on images.
# It takes a list of images, a list of text, and a list of user genereated
# text locations as arguments.

from PIL import Image, ImageDraw, ImageFont # Install Pillow, not PIL

class Imagegenerator():
     def __init__(self,data_list, user_preferences):
          self.image_list, self.text_list=data_list
          self.user_preferences=user_preferences
          
          self.original_image = Image.open(self.image_list[0]+".jpg").convert("RGBA")
          self.x, self.y, self.font_size, self.max_width = 10, 10, 24, self.original_image.size[0] - 20
          self.text_placeholder = Image.new("RGBA", self.original_image.size, (255,255,255,0))
          self.font = ImageFont.truetype("OpenSans-Bold.ttf", self.font_size)
          self.d = ImageDraw.Draw(self.text_placeholder)
          
          self.overlaytext(data_list, user_preferences)
     
     def overlaytext(self,data_list,user_preferences):
          self.image_list, self.text_list=data_list
          self.user_preferences=user_preferences
          
          self.line = ""
          self.lines = []
          self.words = self.text_list[0].split() # Split by whitespace
          for word in self.words:
              if len(self.line.split()) == 0:
                  self.line = word
              else:
                  self.line = "{} {}".format(self.line, word)
              self.line_width, self.line_height = self.d.textsize(self.line, font = self.font)
              if self.line_width > self.max_width:
                  self.last_word = self.line.rsplit(" ", 1)[-1]
                  self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line.rsplit(" ", 1)[0]})
                  self.line = self.last_word
          self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line}) # Catch the last line
          # ...end method (would return lines dict) #
          
          for i, self.line in enumerate(self.lines):
              self.d.text((self.x, self.y + (i * self.line["height"])), self.line["string"], font = self.font, fill = (255,255,255,128)) # To justify right, would set x to original_image.size[0] - line["width"]
          
          self.out = Image.alpha_composite(self.original_image, self.text_placeholder)
          self.out.save(self.image_list[0]+".edit.jpg")          
    