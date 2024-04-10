import os
from TextureColours import *
import style
from appJar import gui
from tkinter import filedialog
from os import getcwd, access, R_OK


def close(app):
    app.close()


class Window:
    global app
    app = gui("BReader")
    filepath = ""
    fileselected = False
    global file
    characterlist = []
    location = 0
    eof = False
    bof = False

    def __init__(self):
        # app = gui("BReader")
        self.initialsetup()
        # app.config(**style.body)
        app.setSize("Fullscreen")
        app.setBg(colour=initStageBg, override=False, tint=False)
        # app.config(**style.body)
        # app.setFg(colour="#d9d9d9", override=True) # CHANGES FOREGROUND PERMANENTLY
        app.setFont(size=60, family="Helvetica")

        app.go()

    def initialsetup(self):

        app.setSticky("se")
        app.addButton("Exit", app.stop, 3, 2).config(**style.button)
        # app.setButtonBg("Exit", buttonBg)
        # app.setButtonFg("Exit", buttonFg)

        app.setSticky("")
        app.addButton("Select file", self.explorefiles, 1, 1, ).config(**style.button)
        # app.setButtonBg("Select file", buttonBg)
        # app.setButtonFg("Select file", buttonFg)

        app.addButton("Confirm selection", self.confirm, 2, 1).config(**style.button)
        # app.setButtonBg("Confirm selection", buttonBg)
        # app.setButtonFg("Confirm selection", buttonFg)

        app.setSticky("nw")
        app.addLabel("Empty", "Cancel", 0, 0)
        app.setLabelFg("Empty", invisible)

        app.setSticky("")
        print("file name: " + os.path.basename(self.filepath))
        app.addLabel("currentfile", "Current file: " + os.path.basename(self.filepath), 0, 1)
        app.setLabelFg("currentfile", labelFg) #for labels the .config command with the style.py does not work I have no idea wahy its just how it is



    def explorefiles(self):
        self.filepath = filedialog.askopenfilename(initialdir=getcwd(), title="Select file",
                                              filetypes=(("all files", "*.*"), ("all files", "*.*")))

        print("File selected")
        if access(self.filepath, R_OK):
            # check to see if file is readable
            # read file
            app.setLabel("currentfile", "Current file: " + os.path.basename(self.filepath))
            print("File is readable")
            self.fileselected = True
            self.file = open(self.filepath, "r")
        else:
            self.openErrorWindow()
            print("Unable to read file\nPlease select a plaintext file")

    def openErrorWindow(win):
        # open new file searcher window
        # defines sub window
        try:
            app.startSubWindow("Error", modal=True, blocking=True)
            app.setBg(colour=initStageBg, override=False, tint=False)
            app.setSize(250, 100)
            app.addLabel("errormsg", "Error:\nFile is not readable \nPlease select a readable file").config(style.error)
            app.setLabelBg("errormsg", labelBg)
            app.setLabelFg("errormsg", labelFg)
            app.setFont()
            app.stopSubWindow()
        except Exception as e:
            print("Error window already defined")
        # displays sub window
        app.showSubWindow("Error")

    def confirm(self):
        if self.fileselected:
            # change layout
            self.initialremove()
            self.scrollersetup()

        else:
            self.openErrorWindow()

    def left(self):
        if self.location == -1:
            app.setLabel("Character Label", "BOF")
        else:
            self.location -= 1
            if self.location == -1:
                app.setLabel("Character Label", "BOF")
            else:
                letter = self.characterlist[self.location]
                app.setLabel("Character Label", letter)

    def right(self):
        if not self.location == -1 and self.characterlist[self.location] == '':
            app.setLabel("Character Label", "EOF")
        else:
            self.location += 1
            if self.location >= len(self.characterlist):
                self.characterlist.append(self.file.read(1))
            if self.characterlist[self.location] == '':
                app.setLabel("Character Label", "EOF")
            else:
                app.setLabel("Character Label", self.characterlist[self.location])

    def initialremove(self):
        app.removeButton("Confirm selection")
        app.removeButton("Select file")
        app.removeLabel("Empty")


    def scrollersetup(self):
        app.addLabel("Character Label", "", 2, 1).config(font=("Helvetica", 80))
        app.setLabelFg("Character Label", labelFg)

        app.addButton(">", self.right, 2, 2).config(style.button)

        app.addButton("<", self.left, 2, 0).config(style.button)

        app.setSticky("nw")
        app.addButton("Cancel", self.scrollertoinitial, 0, 0).config(**style.button)

        app.setSticky("")
        # read first letter
        self.location = -1
        self.characterlist.clear()
        self.left()

    def scrollerremove(self):
        app.removeLabel("Character Label")
        app.removeButton(">")
        app.removeButton("<")
        app.removeButton("Cancel")
        app.removeButton("Exit")
        app.removeLabel("currentfile")

    def scrollertoinitial(self):
        self.scrollerremove()
        self.initialsetup()
window = Window()
