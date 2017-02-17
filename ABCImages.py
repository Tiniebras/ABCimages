# GUI Module for setting user preferences and calling the main script

import os, glob, requests
import main
from appJar import gui

def get_photosets():
    params = {
        "method": "flickr.photosets.getList",
        "user_id": "33625733@N03", # ABC's user_id
        "api_key": "f04a132622fbafbbe31e4521cb553193", # Our API key
        "format": "json",
        "nojsoncallback": "1" # Required for raw JSON https://www.flickr.com/services/api/response.json.html
    }
    try:
        r = requests.get("https://api.flickr.com/services/rest/", params)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit()
    photosets = []
    for photoset in r.json()["photosets"]["photoset"]:
        photosets.append({"title": photoset["title"]["_content"], "id": photoset["id"]})
    return photosets

def press(btn): # function called by pressing the buttons
    with open("userprefs.txt","w") as f:
        fontsize = app.getOptionBox("Font Size:")
        f.write(fontsize + "\n")
        font = app.getOptionBox("Font:")
        f.write(font + "\n")
        fontloc = app.getOptionBox("Text Horizontal Location:")
        f.write(fontloc + "\n")
        fontloc = app.getOptionBox("Text Vertical Location:")
        f.write(fontloc + "\n")
        photoset_index = photoset_titles.index(app.getOptionBox("Flickr Photoset:"))
        photoset_id = photoset_ids[photoset_index]
        f.write(photoset_id + "\n")
    main.main(photoset_id)
    #print(app.getEntry("source"))   
    app.stop()

app = gui()

font_list = glob.glob(os.path.join("fonts", "*.ttf")) # Only list *.ttf files

app.addLabel("title", "ABCImages User Preferences", 0, 0, 2) # Row 0, Column 0, Span 2

photosets = get_photosets()
global photoset_titles, photoset_ids
photoset_titles = [photoset["title"] for photoset in photosets]
photoset_ids = [photoset["id"] for photoset in photosets]
app.addLabelOptionBox("Flickr Photoset:", photoset_titles, 1, 1) # Row 1, Column 1
app.setOptionBox("Flickr Photoset:", 1, value = True)

#app.addLabel("source", "Path or Flickr ID:", 1, 0) # Row 1, Column 0
#app.addEntry("source", 1, 1) # Row 1, Column 1

app.addLabelOptionBox("Font:", font_list, 2, 1) # Row 2, Column 1
app.addLabelOptionBox("Font Size:", ["46","48","50"], 3, 1) # Row 3, Column 1
app.addLabelOptionBox("Text Horizontal Location:", ["Left","Centre","Right"], 4, 1) # Row 4, Column 1
app.addLabelOptionBox("Text Vertical Location:", ["Top","Middle","Bottom"], 5, 1) # Row 5, Column 1
app.setOptionBox("Text Horizontal Location:", 1, value = True)
app.setOptionBox("Text Vertical Location:", 1, value = True)

app.addButtons(["Submit"], press, 6, 0, 2) # Row 3, Column 0,Span 2

#app.setEntryFocus("source")

app.go()
