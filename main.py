# ABC text overlay program
# Imports images from flickr and overlays
# text from a separate source.

#Flicker image loading module - returns
#a list of images and a list of text
import datagrabber


#User input module to set text location
#preferences
import userpreferences

#Image generating module
import imagegenerator

#sys module provides access to command line args. via sys.argv
import sys

   
#Main 
def main(source):
    importsource = source
        
    mydatagrabber = datagrabber.Datagrabber(importsource)
    #data_list = mydatagrabber.getdata_lists()
     
    mypreferences = userpreferences.Userpreferences()
    user_preferences = mypreferences.getuserpreferences()
    
    #myimages = imagegenerator.Imagegenerator(data_list, user_preferences)
    myimages = imagegenerator.Imagegenerator(mydatagrabber, user_preferences)
    
if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1:])
        #else:
        #    print("Photo source path required")
    else:
        main("72157625568426420")

