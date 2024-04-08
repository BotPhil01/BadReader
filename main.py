import os

from appJar import gui
from tkinter import filedialog
from os import getcwd, access, R_OK


def close(app):
    app.close()


class Window:
    global app
    app = gui("BReader")
    global filename
    fileselected = False
    global file
    characterlist = []
    location = 0
    eof = False
    bof = False

    def __init__(self):
        # app = gui("BReader")
        self.initialsetup()
        app.setSize("Fullscreen")
        app.setBg(colour="#424549", override=True)
        app.setHighlightBackground(colour="#424549", override=True)
        app.setFont(size=20, family="Helvetica")
        app.go()

    def initialsetup(self):
        app.setSticky("se")
        app.addButton("Exit", app.stop, 3, 2)
        app.setSticky("")
        app.addButton("Select file", self.explorefiles, 1, 1)
        app.addButton("Confirm selection", self.confirm, 2, 1)
        app.addEmptyLabel("Empty", 0, 0)
        app.addLabel("currentfile", "Current file: ", 0, 1)

    def explorefiles(self):
        filepath = filedialog.askopenfilename(initialdir=getcwd(), title="Select file",
                                              filetypes=(("all files", "*.*"), ("all files", "*.*")))

        print("File selected")
        if access(filepath, R_OK):
            # check to see if file is readable
            # read file
            app.setLabel("currentfile", "Current file: " + filepath)
            print("File is readable")
            self.fileselected = True
            self.file = open(filepath, "r")
        else:
            self.openErrorWindow()
            print("Unable to read file\nPlease select a plaintext file")

    def openErrorWindow(win):
        # open new file searcher window
        # defines sub window
        app.startSubWindow("Error", modal=True, blocking=True)
        app.setSize(250, 100)
        app.addLabel("errormsg", "Error:\nFile is not readable \nPlease select a readable file")
        app.stopSubWindow()
        # displays sub window
        app.showSubWindow("Error")

    def confirm(self):
        if self.fileselected:
            # change layout
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

    def scrollersetup(self):
        app.removeButton("Confirm selection")
        app.removeButton("Select file")
        app.removeLabel("Empty")
        app.addLabel("Character Label", "", 2, 1)
        app.addButton(">", self.right, 2, 2).config(font=("Helvetica", 60), bg="DimGray", fg="Black")
        app.addButton("<", self.left, 2, 0).config(font=("Helvetica", 60), bg="DimGray", fg="Black")
        app.setSticky("nw")
        app.addButton("Cancel", self.scrollertoinitial, 0, 0)
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

    def scrollertoinitial(self):
        self.scrollerremove()
        self.initialsetup()
window = Window()
