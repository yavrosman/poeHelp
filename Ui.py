
import tkinter as tk
from tkinter import ttk

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Path of Exile Helper')
        self.geometry('900x600')  # Total width = menu + app screen + logger
        self.configure(bg='#333333')  # Dark background for the main window
        self.overrideredirect(True)  # Hide window controls and borders

        self.offset_x = 0
        self.offset_y = 0
        self.bind('<Button-1>', self.click_win)
        self.bind('<B1-Motion>', self.drag_win)

        self.menu_frame = tk.Frame(self, width=200, height=600, bg='#333333')
        self.menu_frame.pack(side='left', fill='y')

        self.home_btn = tk.Button(self.menu_frame, text='Home', bg='#FFD700', fg='black',
                                  command=self.show_home)
        self.home_btn.pack(pady=(20, 10), fill='x')

        self.map_craft_btn = tk.Button(self.menu_frame, text='Map Craft', bg='#FFD700', fg='black',
                                       command=self.show_map_craft)
        self.map_craft_btn.pack(pady=10, fill='x')

        self.close_btn = tk.Button(self.menu_frame, text='Close', bg='#FF0000', fg='black',
                                   command=self.close_app)
        self.close_btn.pack(pady=10, fill='x')

        self.app_screen = tk.Frame(self, width=400, height=600, bg='#333333')
        self.app_screen.pack(side='left', fill='y')

        self.logger_panel = tk.Frame(self, width=300, height=600, bg='#333333')
        self.logger_panel.pack(side='left', fill='y')

    def click_win(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag_win(self, event):
        x = self.winfo_pointerx() - self.offset_x
        y = self.winfo_pointery() - self.offset_y
        self.geometry(f'+{x}+{y}')

    def close_app(self):
        self.destroy()

    def show_home(self):
        for widget in self.app_screen.winfo_children():
            widget.destroy()
        home_label = tk.Label(self.app_screen, text="Home Screen", bg='#333333', fg='white')
        home_label.pack(expand=True)

    def show_map_craft(self):
        for widget in self.app_screen.winfo_children():
            widget.destroy()
        map_label = tk.Label(self.app_screen, text="Map Craft Screen", bg='#333333', fg='white')
        map_label.pack(expand=True)
