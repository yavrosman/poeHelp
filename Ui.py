
import tkinter as tk
from tkinter import ttk
from pynput.mouse import Listener as MouseListener
from pynput import mouse
import pyautogui
import pyperclip
import json

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
        
        # Entry for profile name
        self.profile_entry = tk.Entry(self.app_screen, fg='black', bg='white', width=20)
        self.profile_entry.insert(0, 'Profile name')  # Placeholder text
        self.profile_entry.pack(pady=10, side='left', padx=(10, 0))

        # Button to add profile
        self.add_profile_btn = tk.Button(self.app_screen, text='+', bg='#00FF00', fg='black', command=self.create_profile)
        self.add_profile_btn.pack(pady=10, side='left')

        # Display existing profiles
        self.display_profiles()

    def create_profile(self):
        profile_name = self.profile_entry.get()
        if profile_name and profile_name != 'Profile name':
            # Load existing profiles
            try:
                with open('map_craft_profiles.json', 'r') as file:
                    profiles = json.load(file)
            except FileNotFoundError:
                profiles = []

            # Add new profile
            profiles.append({'name': profile_name, 'mods': []})

            # Save to JSON
            with open('map_craft_profiles.json', 'w') as file:
                json.dump(profiles, file, indent=4)
            
            # Update UI
            self.display_profiles()

    def display_profiles(self):
        # Assuming there is a frame for displaying profiles
        if hasattr(self, 'profiles_frame'):
            self.profiles_frame.destroy()
        
        self.profiles_frame = tk.Frame(self.app_screen, bg='#333333')
        self.profiles_frame.pack(fill='both', expand=True)
        
        try:
            with open('map_craft_profiles.json', 'r') as file:
                profiles = json.load(file)
        except FileNotFoundError:
            profiles = []

        for profile in profiles:
            label = tk.Label(self.profiles_frame, text=profile['name'], bg='white', fg='black')
            label.pack(pady=2, padx=10, fill='x')

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            pyautogui.hotkey('ctrl', 'alt', 'c')
            clipboard_content = pyperclip.paste()
            item_name, modifiers = self.parse_item_data(clipboard_content)
            if item_name and modifiers:
                self.print_to_logger(item_name, modifiers)

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

    def print_to_logger(self, item_name, modifiers):
        # Clear existing content
        for widget in self.logger_panel.winfo_children():
            widget.destroy()
        
        # Item name in bold and yellow
        item_label = tk.Label(self.logger_panel, text=item_name, bg='#333333', fg='#FFD700', font=('Helvetica', '12', 'bold'))
        item_label.pack()

        # Modifiers
        for mod in modifiers:
            mod_label = tk.Label(self.logger_panel, text=mod, bg='#333333', fg='white')
            mod_label.pack()

    def parse_item_data(self, clipboard_content):
        sections = clipboard_content.split('--------')
        if len(sections) < 5:
            return None, None  # Not enough data

        # Extracting item name (last line of the first block)
        item_name = sections[0].strip().split('\n')[-1]

        # Extracting modifiers (everything in the fifth section), excluding lines between "{}"
        modifiers = [line.strip() for line in sections[4].strip().split('\n') if not (line.startswith('{') and line.endswith('}'))]

        return item_name, modifiers

