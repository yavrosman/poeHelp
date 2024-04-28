
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Listener as MouseListener
from pynput import mouse
import pyautogui
import pyperclip

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

        # Menu Frame with border
        self.menu_frame = tk.Frame(self, width=200, height=600, bg='#333333', bd=2, relief='solid')
        self.menu_frame.pack(side='left', fill='y')
        self.menu_frame.pack_propagate(False)  # Prevent resizing

        # Buttons are centered by using padx and pady for uniform spacing around
        self.home_btn = tk.Button(self.menu_frame, text='Home', bg='#FFD700', fg='black',
                                  command=self.show_home)
        self.home_btn.pack(pady=(60, 10), padx=20, fill='x')

        self.map_craft_btn = tk.Button(self.menu_frame, text='Map Craft', bg='#FFD700', fg='black',
                                       command=self.show_map_craft)
        self.map_craft_btn.pack(pady=10, padx=20, fill='x')

        self.close_btn = tk.Button(self.menu_frame, text='Close', bg='#FF0000', fg='black',
                                   command=self.close_app)
        self.close_btn.pack(pady=10, padx=20, fill='x')

        # Main App Screen with border
        self.app_screen = tk.Frame(self, width=400, height=600, bg='#333333', bd=2, relief='solid')
        self.app_screen.pack(side='left', fill='y')
        self.app_screen.pack_propagate(False)  # Prevent resizing


        # Logger Panel with border
        self.logger_panel = tk.Frame(self, width=400, height=600, bg='#333333', bd=2, relief='solid')
        self.logger_panel.pack(side='left', fill='y')
        self.logger_panel.pack_propagate(False)  # Prevent resizing


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
        self.data_fetch_btn = tk.Button(self.app_screen, text="Enable Data Fetching", bg='#FFD700', fg='black',
                                        command=self.toggle_data_fetch)
        self.data_fetch_btn.pack(pady=10, fill='x')
        map_label = tk.Label(self.app_screen, text="Map Craft Screen", bg='#333333', fg='white')
        map_label.pack(expand=True)

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            pyautogui.hotkey('ctrl', 'alt', 'c')
            clipboard_content = pyperclip.paste()
            self.print_to_logger(clipboard_content)

    def toggle_data_fetch(self):
        if self.data_fetch_btn['bg'] == '#FFD700':  # Yellow means inactive
            self.data_fetch_btn['bg'] = '#00FF00'  # Green means active
            self.start_listening()
        else:
            self.data_fetch_btn['bg'] = '#FFD700'
            self.stop_listening()
    
    def start_listening(self):
        self.listener = MouseListener(on_click=self.on_click)
        self.listener.start()

    def stop_listening(self):
        self.listener.stop()

    def print_to_logger(self, text):
        # Clear existing content
        for widget in self.logger_panel.winfo_children():
            widget.destroy()
        log_label = tk.Label(self.logger_panel, text=text, bg='#333333', fg='white')
        log_label.pack()
