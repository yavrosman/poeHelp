#import tkinter as tk
from tkinter import Frame, Label, Button, Text

# Set up dark theme colors
bg = '#333' # dark gray
txt_bg = '#444' # lighter gray
btn_bg(active)= '#fff' # button active color (green)
btn_bg(unactive)= '#ff0' # button unactive color (yellow)

root = tk.Tk()
root.title('POE Helper Tool')
root.configure(bg_bg=bg)

menu_panel = Frame(root, bg_bg='#ff0', height=500, width=200)
menu_panel.pack(side='left', pady=10)

home_btn = Button(menu_panel, text='Home', bg=btn_bg('active'), command=lambda: home_btn.config(bg=btn_bg('inactive')))
home_btn.pack(side='top', pady=5)

close_btn = Button(menu_panel, text='Close', bg_bg='red', command=root.destroy)
close_btn.pack(side='bottom', pady=5)

main_screen = Frame(root, bg_bg='black', width=400)
main_screen.pack(side='left', pady=10)

logger_panel = Text(root, bg_bg=txt_bg, height=500, width=150)
logger_panel.pack(side='right', pady=10)