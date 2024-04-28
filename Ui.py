import tkinter as Tk
from tkinter import *

class App(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('POE Helper Tool')
        label = Label(self.root, text='Hello, Path of Exile Helper')
        label.pack()

    def run(self):
        self.root.mainloop()

def create_gui():
    app = App()
    app.run()
