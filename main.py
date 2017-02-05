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
user_preferences = {"font_size": 48}

#data_list = (["5248291471", "5248866198", "5248867544", "5248874566"], ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."])

myimages = imagegenerator.Imagegenerator(data_list, user_preferences)

