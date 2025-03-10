from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from datetime import datetime, date
from kivy.metrics import dp
import json
import os

# Set window size for testing (will be ignored in mobile)
Window.size = (400, 700)

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Store data
try:
    store = JsonStore('data/medicine_data.json')
except Exception as e:
    print(f"Error creating store: {e}")
    store = JsonStore('data/medicine_data.json', indent=2)

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.current_index = 0
        self.time_slots = ["Morning", "Afternoon", "Evening", "Night"]
        
        try:
            # Header with title and date
            header = MDCard(
                orientation="vertical",
                size_hint=(1, None),
                height="80dp",
                padding="8dp",
                spacing="4dp",
                elevation=2,
                radius=[0, 0, 0, 0],
                pos_hint={"top": 1},  # Position at the very top
                md_bg_color=(0, 0.6, 0.4, 1)  # Teal color
            )
            
            # Title
            title = MDLabel(
                text="Medicine Tracker",
                font_style="H6",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            header.add_widget(title)
            
            # Date
            self.date_label = MDLabel(
                text=datetime.now().strftime("%B %d, %Y"),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.8),
                halign="center"
            )
            header.add_widget(self.date_label)
            self.add_widget(header)
            
            # Time slot label in a card - positioned right below header
            time_slot_card = MDCard(
                orientation="vertical",
                size_hint=(1, None),  # Full width
                height="100dp",
                pos_hint={"center_x": 0.5, "top": 0.856},  # Positioned right below header
                padding="16dp",
                elevation=1,
                radius=[0, 0, 0, 0],  # No radius for seamless look
                md_bg_color=(0.85, 0.85, 0.85, 1)
            )
            
            self.time_slot_label = MDLabel(
                text=self.time_slots[self.current_index],
                font_style="H4",
                halign="center",
                theme_text_color="Primary"
            )
            time_slot_card.add_widget(self.time_slot_label)
            self.add_widget(time_slot_card)
            
            # Status buttons
            self.taken_button = MDRaisedButton(
                text="TAKEN",
                pos_hint={"center_x": 0.5, "center_y": 0.6},
                size_hint=(0.8, None),
                height="56dp",
                md_bg_color=(0.5, 0.5, 0.5, 1)  # Gray color
            )
            self.taken_button.bind(on_press=lambda x: self.toggle_status(True))
            self.add_widget(self.taken_button)
            
            self.not_taken_button = MDRaisedButton(
                text="NOT TAKEN",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                size_hint=(0.8, None),
                height="56dp",
                md_bg_color=(0.8, 0, 0, 1)  # Red color
            )
            self.not_taken_button.bind(on_press=lambda x: self.toggle_status(False))
            self.add_widget(self.not_taken_button)
            
            # Navigation buttons
            nav_buttons = MDCard(
                orientation="horizontal",
                size_hint=(0.8, None),
                height="56dp",
                pos_hint={"center_x": 0.5, "center_y": 0.4},
                padding="8dp",
                spacing="8dp",
                elevation=0,
                md_bg_color=(0, 0, 0, 0)
            )
            
            prev_button = MDFlatButton(
                text="PREVIOUS",
                size_hint=(0.5, 0.900),
                on_press=self.previous_slot
            )
            next_button = MDFlatButton(
                text="NEXT",
                size_hint=(0.5, 0.900),
                on_press=self.next_slot
            )
            
            nav_buttons.add_widget(prev_button)
            nav_buttons.add_widget(next_button)
            self.add_widget(nav_buttons)
            
            # Stats button
            stats_button = MDRaisedButton(
                text="VIEW STATISTICS",
                pos_hint={"center_x": 0.5, "center_y": 0.186},
                size_hint=(0.8, None),
                height="56dp",
                md_bg_color=(0, 0.6, 0.4, 1)  # Teal color
            )
            stats_button.bind(on_press=self.show_stats)
            self.add_widget(stats_button)
            
            # Update status on init
            self.update_status()
            
        except Exception as e:
            print(f"Error initializing MainScreen: {e}")
    
    def toggle_status(self, taken):
        try:
            today = date.today().isoformat()
            current_slot = self.time_slots[self.current_index]
            
            if not store.exists(today):
                store.put(today, Morning=False, Afternoon=False, Evening=False, Night=False)
            
            day_data = store.get(today)
            day_data[current_slot] = taken
            store.put(today, **day_data)
            
            self.update_status()
            
        except Exception as e:
            print(f"Error toggling status: {e}")
    
    def update_status(self):
        try:
            today = date.today().isoformat()
            current_slot = self.time_slots[self.current_index]
            
            if store.exists(today):
                taken = store.get(today).get(current_slot, False)
                if taken:
                    self.taken_button.md_bg_color = (0, 0.7, 0, 1)  # Green
                    self.not_taken_button.md_bg_color = (0.5, 0.5, 0.5, 1)  # Gray
                else:
                    self.taken_button.md_bg_color = (0.5, 0.5, 0.5, 1)  # Gray
                    self.not_taken_button.md_bg_color = (0.8, 0, 0, 1)  # Red
            
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def next_slot(self, instance):
        self.current_index = (self.current_index + 1) % len(self.time_slots)
        self.time_slot_label.text = self.time_slots[self.current_index]
        self.update_status()
    
    def previous_slot(self, instance):
        self.current_index = (self.current_index - 1) % len(self.time_slots)
        self.time_slot_label.text = self.time_slots[self.current_index]
        self.update_status()
    
    def show_stats(self, instance):
        self.parent.current = "stats"

class StatsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "stats"
        
        try:
            # Container card for stats
            stats_card = MDCard(
                orientation="vertical",
                size_hint=(0.9, None),
                height="400dp",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                padding="16dp",
                spacing="8dp",
                elevation=2,
                radius=[20, 20, 20, 20]
            )
            
            # Title
            stats_title = MDLabel(
                text="Statistics",
                font_style="H5",
                halign="center",
                size_hint_y=None,
                height="48dp"
            )
            stats_card.add_widget(stats_title)
            
            # Stats content
            self.stats_label = MDLabel(
                text="Loading stats...",
                halign="center",
                theme_text_color="Secondary"
            )
            stats_card.add_widget(self.stats_label)
            
            # Back button
            back_button = MDFlatButton(
                text="BACK TO TRACKER",
                pos_hint={"center_x": 0.5},
                on_press=self.go_back
            )
            stats_card.add_widget(back_button)
            
            self.add_widget(stats_card)
            self.bind(on_enter=self.update_stats)
            
        except Exception as e:
            print(f"Error initializing StatsScreen: {e}")
    
    def go_back(self, instance):
        self.parent.current = "main"
    
    def update_stats(self, instance):
        try:
            total_doses = 0
            total_taken = 0
            days_tracked = 0
            
            for key in store.keys():
                days_tracked += 1
                day_data = store.get(key)
                total_doses += 4
                total_taken += sum(1 for value in day_data.values() if value)
            
            if days_tracked == 0:
                stats_text = "No data recorded yet"
            else:
                adherence = (total_taken / total_doses) * 100
                stats_text = f"""Days Tracked: {days_tracked}

Total Doses Taken: {total_taken} out of {total_doses}

Adherence Rate: {adherence:.1f}%

Keep up the good work!"""
            
            self.stats_label.text = stats_text
        except Exception as e:
            print(f"Error updating stats: {e}")
            self.stats_label.text = "Error loading statistics"

class MedicineTrackerApp(MDApp):
    def build(self):
        try:
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.accent_palette = "Blue"
            self.theme_cls.theme_style = "Light"
            
            sm = ScreenManager()
            sm.add_widget(MainScreen())
            sm.add_widget(StatsScreen())
            
            return sm
        except Exception as e:
            print(f"Error building app: {e}")
            return None

if __name__ == "__main__":
    MedicineTrackerApp().run()