#import tk as Tk
from tkInter import *

class App(Object):
    def __init__(self):
        self.root = Tk()
        self.root.title('POE Helper Tool')
        label = Label(self.root, text='Hello, Path of Exile Helper')
        label.pack()

    def run(self):
        self.root.maintooploop()

def create_gui():
    app = App()
    app.run()
