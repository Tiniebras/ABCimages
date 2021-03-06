# Module containing the Datagrabber class which grabs images and text from
# selected sources and dumps them to the local drive.
#
# getdata_list provides a list of the images names and a list of the texts.
# getimages grabs images from the chosen source and adds them to the list.
#
# Source options are flicker, or local so that we dont have to download them
# more than once.

import os, requests, sys, shutil

class Datagrabber():
    def __init__(self,source):
        
        #image and text lists to be populated
        self.image_list = []
        self.text_list = []
        
        self.loadimages(source)
        self.loadtext()
    
    def getdata_lists(self):
        return (self.image_list, self.text_list)
    
    def gettext(self,i):
        return (self.text_list[i])
    
    def gettextlen(self):
        return (len(self.text_list))
    
    def getimage(self, i):
        return (self.image_list[i])
    
    def loadimages(self,source):
        #Grab images from path
        if os.path.exists(source):
            self.__local()        
        #Grab images from flickr
        else:
            self.__flickr(source)       

    def __flickr(self,source):
        self.photoset_id = source
        self.params = {
            "method": "flickr.photosets.getPhotos",
            "photoset_id": self.photoset_id, #"72157625568426420", # Using 'Boats in the Baptistry' for now
            "user_id": "33625733@N03", # ABC's user_id
            "api_key": "f04a132622fbafbbe31e4521cb553193", # Our API key
            "format": "json",
            "nojsoncallback": "1" # Required for raw JSON https://www.flickr.com/services/api/response.json.html
        }

        try:
            self.r = requests.get("https://api.flickr.com/services/rest/", self.params)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit()

        self.urls = {}

        for photo in self.r.json()["photoset"]["photo"]:
            self.urls[photo["id"]] = "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_b.jpg".\
                format(**photo) # Info on Flickr URLs: https://www.flickr.com/services/api/misc.urls.html
    
        #urlkeys is a dict_keys object so must be type cast to a list
        self.image_list = self.image_list + list(self.urls.keys())
        
        for id, url in self.urls.items():
            if not os.path.isfile(os.path.join("photos", id + ".jpg")):
                try:
                    self.r = requests.get(url, stream = True)
                    with open(os.path.join("photos", "{}.jpg".format(id)), "wb") as out_file:
                        shutil.copyfileobj(self.r.raw, out_file)
                    del self.r
                    print("Downloaded {}.jpg".format(id))
                except requests.exceptions.RequestException as e:
                    print(e)
                    sys.exit()
            else:
                print(id + ".jpg already exists")

    def __local(self):
        self.info = "to be done"
        
    def loadtext(self):
        try:
            with open("quotes.txt") as self.f:
                self.text_list = self.text_list + self.f.readlines()
        except Exception:
            print("failed to load quotes.txt")


#source="flickr"
#mydatagrabber = Datagrabber(source)



