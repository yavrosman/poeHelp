from PyQt5.QtWidgets import QMainWindow,QLabel, QHBoxLayout, QListWidget, QFrame, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt  # Add this line
from pynput import mouse
import pyautogui
import pyperclip
import time
import json
from PyQt5.QtWidgets import QApplication,QListWidgetItem, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit
import re
from PyQt5.QtGui import QColor  # Add this line

class ModsWindow(QMainWindow):
    def __init__(self, profile_name):
        super(ModsWindow, self).__init__()
        self.profile_name = profile_name
        self.mods = []

        # Load the profile data from the JSON file
        with open("map_craft_profiles.json", "r") as file:
            profiles = json.load(file)
        for profile in profiles:
            if profile["name"] == profile_name:
                self.mods = profile["mods"]
                break

        self.setWindowTitle(profile_name)
        self.setFixedSize(900, 500)

        self.title = QLabel(profile_name)
        self.title.setStyleSheet("background-color: #3c3f41; color: #f0e68c; font-size: 20px; font-weight: bold;")
        self.title.setFixedHeight(50)
        self.title.setAlignment(Qt.AlignCenter)

        self.mods_list = QListWidget()
        self.mods_list.setFixedWidth(400)

        # Define selected_mods_list and connect itemClicked signal
        self.selected_mods_list = QListWidget(self)
        self.selected_mods_list.itemClicked.connect(self.on_item_clicked)

        self.border = QFrame()
        self.border.setFrameShape(QFrame.VLine)
        self.border.setFrameShadow(QFrame.Sunken)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.mods_list)
        self.layout.addWidget(self.border)
        self.layout.addWidget(self.selected_mods_list)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title)
        self.main_layout.addLayout(self.layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

        # Populate the mods list after everything is set up
        for mod in self.mods:
            self.mods_list.addItem(mod)

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.middle and pressed:
            self.selected_mods_list.clear()
            pyautogui.hotkey('ctrl', 'alt', 'c')
            item_data = pyperclip.paste()
            cleaned_modifiers = self.extract_modifiers(item_data)
            if cleaned_modifiers:
                for mod in cleaned_modifiers.split('\n'):
                    item = QListWidgetItem(mod)
                    if mod in self.mods:
                        item.setBackground(QColor('green'))
                    self.selected_mods_list.addItem(item)
                print(f"Item Count: {self.selected_mods_list.count()}")  # Debug print statement

    def on_item_clicked(self, item):
        mod = item.text()
        if mod in self.mods:
            # Remove the mod from self.mods and self.mods_list
            self.mods.remove(mod)
            for i in range(self.mods_list.count()):
                if self.mods_list.item(i).text() == mod:
                    self.mods_list.takeItem(i)
                    break

            # Remove the green background from the corresponding item in self.selected_mods_list
            for i in range(self.selected_mods_list.count()):
                if self.selected_mods_list.item(i).text() == mod:
                    self.selected_mods_list.item(i).setBackground(QColor('white'))
                    break
        else:
            # Add the mod to self.mods and self.mods_list
            item.setBackground(QColor('green'))
            self.mods.append(mod)
            self.mods_list.addItem(mod)

        # Save the profile data back to the JSON file
        with open("map_craft_profiles.json", "r") as file:
            profiles = json.load(file)
        for profile in profiles:
            if profile["name"] == self.profile_name:
                profile["mods"] = self.mods
                break
        with open("map_craft_profiles.json", "w") as file:
            json.dump(profiles, file)

    def closeEvent(self, event):
        # Stop the listener when the window is closed
        self.listener.stop()
        event.accept()

    @staticmethod
    def extract_modifiers(item_data):
        # Extract everything after "Monster Level: *number*"
        modifiers_section = re.search(r'Monster Level: \d+\s*(.*)', item_data, re.DOTALL)
        if modifiers_section:
            modifiers = modifiers_section.group(1)
            # Extract everything before the second last "--------"
            modifiers_section = re.search(r'(.*)(--------.*--------)', modifiers, re.DOTALL)
            if modifiers_section:
                modifiers = modifiers_section.group(1)
                # Remove the strings inside "{}"
                cleaned_modifiers = re.sub(r'\{.*?\}', '', modifiers)
                cleaned_modifiers = re.sub(r'--------', '', cleaned_modifiers)
                # Remove empty lines
                cleaned_modifiers = "\n".join(line for line in cleaned_modifiers.split('\n') if line.strip())
                return cleaned_modifiers.strip()

        return None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("POE Helper Tool")

        # Set the overall style to a dark theme
        self.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6; font-size: 14px;")

        # Menu Panel
        self.menu_panel = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu_panel.setLayout(self.menu_layout)
        self.menu_panel.setFixedWidth(200)

        self.menu_title = QLabel("Menu")
        self.home_btn = QPushButton("Home")
        self.maps_btn = QPushButton("Maps")
        self.close_btn = QPushButton("Close")

        self.menu_layout.addWidget(self.menu_title)
        self.menu_layout.addWidget(self.home_btn)
        self.menu_layout.addWidget(self.maps_btn)
        self.menu_layout.addStretch(1)
        self.menu_layout.addWidget(self.close_btn)

        # Route Panel
        self.route_panel = QWidget()
        self.route_layout = QVBoxLayout()
        self.route_panel.setLayout(self.route_layout)
        self.route_panel.setFixedWidth(500)

        self.route_title = QLabel("Home")
        self.route_title.setStyleSheet("background-color: #3c3f41; color: #f0e68c; font-size: 20px; font-weight: bold;")
        self.route_title.setFixedHeight(50)
        self.route_title.setAlignment(Qt.AlignCenter)
        self.route_layout.addWidget(self.route_title, alignment=Qt.AlignTop)

        # Craft Panel
        self.craft_panel = QWidget()
        self.craft_layout = QVBoxLayout()
        self.craft_panel.setLayout(self.craft_layout)

        self.profile_label = QLabel("Create Profile")
        self.profile_input = QLineEdit()
        self.create_btn = QPushButton("Create")
        self.craft_layout.addWidget(self.profile_label)
        self.craft_layout.addWidget(self.profile_input)
        self.craft_layout.addWidget(self.create_btn)

        self.profile_table = QTableWidget()
        self.profile_table.setColumnCount(4)
        self.profile_table.setHorizontalHeaderLabels(["Name", "", "", ""])
        self.profile_table.horizontalHeader().setStyleSheet("color: #000000;")
        self.profile_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.craft_layout.addWidget(self.profile_table)

        # Logger Panel
        self.logger_panel = QTextEdit()
        self.logger_title = QLabel("Logger")

        self.logger_layout = QVBoxLayout()
        self.logger_layout.addWidget(self.logger_title)
        self.logger_layout.addWidget(self.logger_panel)
        self.logger_panel.setFixedWidth(300)

        # Main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.menu_panel)
        self.main_layout.addWidget(self.route_panel)
        self.main_layout.addWidget(self.logger_panel)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        # Connect buttons
        self.home_btn.clicked.connect(self.on_home_clicked)
        self.maps_btn.clicked.connect(self.on_maps_clicked)
        self.close_btn.clicked.connect(self.close)
        self.create_btn.clicked.connect(self.on_create_clicked)

        # Set Home as default
        self.on_home_clicked()

        # Print "Initialized" in the logger panel
        self.logger_panel.append("Initialized")

    def on_home_clicked(self):
        # Change button color
        self.home_btn.setStyleSheet("background-color: #3c3f41; color: #a9b7c6;")
        self.maps_btn.setStyleSheet("background-color: #3c3f41; color: #a9b7c6;")
        self.close_btn.setStyleSheet("background-color: #3c3f41; color: #a9b7c6;")

        # Change route title
        self.route_title.setText("Home")

        # Remove the craft panel
        if self.craft_panel in self.route_layout.children():
            self.route_layout.removeWidget(self.craft_panel)
            self.craft_panel.hide()

    def on_maps_clicked(self):
        # Change button color
        self.home_btn.setStyleSheet("background-color: #3c3f41; color: #a9b7c6;")
        self.maps_btn.setStyleSheet("background-color: #3c3f41; color: #a9b7c6;")
        self.close_btn.setStyleSheet("background-color: #3c3f41; color: #a9b7c6;")

        # Change route title
        self.route_title.setText("Maps")

        # Show the craft panel
        self.route_layout.addWidget(self.craft_panel)
        self.craft_panel.show()

        # Refresh the profile table
        self.refresh_profile_table()

    def on_create_clicked(self):
        # Get the profile name from the input
        profile_name = self.profile_input.text()

        # Create a new profile
        new_profile = {
            "name": profile_name,
            "mods": [],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Load the existing profiles from the JSON file
        with open("map_craft_profiles.json", "r") as file:
            profiles = json.load(file)

        # Add the new profile to the list
        profiles.append(new_profile)

        # Save the updated list back to the JSON file
        with open("map_craft_profiles.json", "w") as file:
            json.dump(profiles, file)

        # Add the new profile to the table
        row = self.profile_table.rowCount()
        self.profile_table.insertRow(row)
        self.profile_table.setItem(row, 0, QTableWidgetItem(profile_name))
        select_btn = QPushButton("Select")
        select_btn.clicked.connect(lambda: self.on_select_clicked(profile_name, select_btn))
        self.profile_table.setCellWidget(row, 1, select_btn)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.on_delete_clicked(profile_name))
        self.profile_table.setCellWidget(row, 2, delete_btn)

    def on_select_clicked(self, profile_name, select_btn):
        # Set the selected profile
        self.selected_profile = profile_name

        # Change the button color
        select_btn.setStyleSheet("background-color: #008000; color: #ffffff;")

        # Print a message in the logger panel
        self.logger_panel.append(f"Profile: {profile_name} Selected!")

    def on_delete_clicked(self, profile_name):
        # Load the existing profiles from the JSON file
        with open("map_craft_profiles.json", "r") as file:
            profiles = json.load(file)

        # Remove the profile from the list
        profiles = [profile for profile in profiles if profile["name"] != profile_name]

        # Save the updated list back to the JSON file
        with open("map_craft_profiles.json", "w") as file:
            json.dump(profiles, file)

        # Remove the profile from the table
        for row in range(self.profile_table.rowCount()):
            if self.profile_table.item(row, 0).text() == profile_name:
                self.profile_table.removeRow(row)
                break

    def refresh_profile_table(self):
        # Load the existing profiles from the JSON file
        with open("map_craft_profiles.json", "r") as file:
            profiles = json.load(file)

        # Clear the table
        self.profile_table.setRowCount(0)

        # Add the profiles to the table
        for profile in profiles:
            row = self.profile_table.rowCount()
            self.profile_table.insertRow(row)
            self.profile_table.setItem(row, 0, QTableWidgetItem(profile["name"]))
            select_btn = QPushButton("Select")
            select_btn.clicked.connect(lambda: self.on_select_clicked(profile["name"], select_btn))
            self.profile_table.setCellWidget(row, 1, select_btn)
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda: self.on_delete_clicked(profile["name"]))
            self.profile_table.setCellWidget(row, 2, delete_btn)
            mods_btn = QPushButton("Mods")
            mods_btn.clicked.connect(lambda: self.on_mods_clicked(profile["name"]))
            self.profile_table.setCellWidget(row, 3, mods_btn)

    def on_mods_clicked(self, profile_name):
        self.mods_window = ModsWindow(profile_name)
        self.mods_window.show()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()