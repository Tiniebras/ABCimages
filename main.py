# ABC text overlay program
# Imports images from flickr and overlays
# text from a separate source.

#Flicker image loading module - returns
#a list of images and a list of text
import datagrabber


#User input module to set text location
#preferences
#import userpreferences

#Image generating module
import imagegenerator

#Main 
mydatagrabber = datagrabber.Datagrabber("flickr")
data_list = mydatagrabber.getdata_lists()
 
#mypreferences = userpreferences.Userpreferences(data_list)
#user_preferences = mypreferences.getpreferences()
user_preferences = {"font_size": 48, "font": "random"}
#user_preferences = {"font_size": 48, "font": "OpenSans-Bold.ttf"}

myimages = imagegenerator.Imagegenerator(data_list, user_preferences)

