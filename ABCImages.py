# GUI Module for setting user preferences and calling the main script

from appJar import gui

#Get font list in fonts folder
import os

#Import main
import main

# function called by pressing the buttons
def press(btn):
    with open("userprefs.txt","w") as f:
        f.truncate()
        fontsize= app.getOptionBox("Font Size:")
        f.write(fontsize + "\n")
        font = app.getOptionBox("Font:")
        f.write(font + "\n")
        fontloc = app.getOptionBox("Text Location:")
        f.write(fontloc + "\n")
    main.main(app.getEntry("source"))
    #print(app.getEntry("source"))   
    app.stop()

    
app = gui()

font_list = os.listdir("fonts")

app.addLabel("title", "ABCImages User Preferences", 0, 0, 2)    # Row 0,Column 0,Span 2
app.addLabel("source", "Path or Fliker ID:", 1, 0)              # Row 1,Column 0
app.addEntry("source", 1, 1)                                    # Row 1,Column 1

app.addLabelOptionBox("Font:", font_list, 2, 1)              # Row 2,Column 1
app.addLabelOptionBox("Font Size:", ["46","48","50"], 3, 1)        # Row 3,Column 1
app.addLabelOptionBox("Text Location:", ["- Top -", "Left","Centre","Right",
                        "- Centre -", "Left","Centre","Right",
                        "- Bottom -", "Left","Centre","Right"], 4, 1)# Row 3,Column 1
app.setOptionBox("Text Location:", 1, value=True)

app.addButtons(["Submit"], press, 5, 0, 2)            # Row 3,Column 0,Span 2

app.setEntryFocus("source")

app.go()