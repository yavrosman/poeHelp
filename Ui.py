import tkinter as tk
from tkinter import Frame, Label, Button, Text


def create_gui():
    root = tk.Tk()
    root.title('POE Helper Tool')

    # Set up dark theme colors
    bg = '#333'  # dark gray
    txt_bg = '#444'  # lighter gray
    btn_bg_active = '#fff'  # button active color (green)
    btn_bg_inactive = '#ff0'  # button inactive color (yellow)

    root.configure(bg=bg)

    menu_panel = Frame(root, bg='#ff0', height=500, width=200)
    menu_panel.pack(side='left', pady=10)

    home_btn = Button(menu_panel, text='Home', bg=btn_bg_active, command=lambda: home_btn.config(bg=btn_bg_inactive))
    home_btn.pack(side='top', pady=5)

    close_btn = Button(menu_panel, text='Close', bg='red', command=root.destroy)
    close_btn.pack(side='bottom', pady=5)

    main_screen = Frame(root, bg='black', width=400)
    main_screen.pack(side='left', pady=10)

    logger_panel = Text(root, bg=txt_bg, height=500, width=150)
    logger_panel.pack(side='right', pady=10)

    root.mainloop()