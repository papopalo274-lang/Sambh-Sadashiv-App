import os
import sqlite3
import random
from datetime import datetime

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.utils import platform

# Android Native Beep Sound
if platform == 'android':
    try:
        from jnius import autoclass
        ToneGenerator = autoclass('android.media.ToneGenerator')
        AudioManager = autoclass('android.media.AudioManager')
        tone_gen = ToneGenerator(AudioManager.STREAM_MUSIC, 80)
    except Exception:
        tone_gen = None
else:
    tone_gen = None

# 1. DATABASE MANAGEMENT
def get_db_path():
    if platform == 'android':
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), "jaap_tracker.db")
    return "jaap_tracker.db"

DB_NAME = get_db_path()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jaap_records (
            date TEXT PRIMARY KEY,
            count INTEGER,
            last_updated TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_today_count():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM jaap_records WHERE date = ?", (today,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def save_today_count(count):
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jaap_records (date, count, last_updated)
        VALUES (?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET count=?, last_updated=?
    ''', (today, count, now_time, count, now_time))
    conn.commit()
    conn.close()

def get_total_lifetime_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(count) FROM jaap_records")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def reset_db_counts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jaap_records")
    conn.commit()
    conn.close()

# 2. FLOWER ANIMATION WIDGET
class FlowerRainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.petals = []

    def trigger_flowers(self):
        for _ in range(30):
            x = random.randint(20, int(self.width) - 20) if self.width > 40 else 100
            y = self.height + random.randint(10, 100)
            vx = random.uniform(-1.5, 1.5)
            vy = random.uniform(-6, -3)
            color = random.choice([
                (0.9, 0.1, 0.3, 0.9),  # Red
                (1.0, 0.6, 0.0, 0.9),  # Orange
                (1.0, 0.84, 0.0, 0.9)  # Yellow
            ])
            self.petals.append([x, y, vx, vy, color])

        Clock.unschedule(self.animate)
        Clock.schedule_interval(self.animate, 1.0 / 30.0)

    def animate(self, dt):
        self.canvas.clear()
        new_petals = []
        with self.canvas:
            for p in self.petals:
                x, y, vx, vy, color = p
                x += vx
                y += vy
                if y > 0:
                    Color(*color)
                    Ellipse(pos=(x, y), size=(12, 18))
                    new_petals.append([x, y, vx, vy, color])

        self.petals = new_petals
        if not self.petals:
            Clock.unschedule(self.animate)
            self.canvas.clear()

# 3. MAIN APP INTERFACE
class SambhSadashivApp(App):
    def build(self):
        init_db()
        self.current_count = get_today_count()

        root = FloatLayout()

        self.flower_widget = FlowerRainWidget(size_hint=(1, 1))
        root.add_widget(self.flower_widget)

        box = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))

        self.clock_label = Label(text="", font_size='16sp', color=(1, 0.84, 0, 1), size_hint=(1, 0.1))
        box.add_widget(self.clock_label)

        title_label = Label(text="— आज का नाम जाप —", font_size='20sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, 0.1))
        box.add_widget(title_label)

        self.count_label = Label(text=str(self.current_count), font_size='54sp', bold=True, color=(0, 1, 0.8, 1), size_hint=(1, 0.2))
        box.add_widget(self.count_label)

        mala_count = self.current_count // 108
        self.mala_label = Label(
            text=f"माला पूर्ण: {mala_count}  |  कुल जाप: {get_total_lifetime_count()}",
            font_size='15sp',
            color=(1, 0.84, 0, 1),
            size_hint=(1, 0.1)
        )
        box.add_widget(self.mala_label)

        self.mantra_label = Label(text="", font_size='24sp', bold=True, color=(0.2, 0.8, 1, 1), size_hint=(1, 0.15))
        box.add_widget(self.mantra_label)

        self.jaap_btn = Button(
            text="✨ साम्ब सदाशिव ✨",
            font_size='22sp',
            bold=True,
            background_color=(0.02, 0.5, 0.8, 1),
            size_hint=(1, 0.18)
        )
        self.jaap_btn.bind(on_press=self.on_jaap_click)
        box.add_widget(self.jaap_btn)

        reset_btn = Button(
            text="🔄 रीसेट (Reset)",
            font_size='14sp',
            background_color=(0.9, 0.2, 0.2, 1),
            size_hint=(0.4, 0.07),
            pos_hint={'center_x': 0.5}
        )
        reset_btn.bind(on_press=self.reset_counter)
        box.add_widget(reset_btn)

        root.add_widget(box)
        Clock.schedule_interval(self.update_clock, 1)

        return root

    def update_clock(self, dt):
        now = datetime.now()
        self.clock_label.text = now.strftime("⏰ %I:%M:%S %p | 📅 %d %b %Y")

    def play_sound(self):
        if platform == 'android' and tone_gen:
            try:
                tone_gen.startTone(ToneGenerator.TONE_PROP_BEEP, 80)
            except Exception:
                pass

    def hide_mantra(self, dt):
        self.mantra_label.text = ""

    def on_jaap_click(self, instance):
        self.current_count += 1
        save_today_count(self.current_count)

        mala_count = self.current_count // 108
        self.count_label.text = str(self.current_count)
        self.mala_label.text = f"माला पूर्ण: {mala_count}  |  कुल जाप: {get_total_lifetime_count()}"

        self.mantra_label.text = "🌸 साम्ब सदाशिव 🌸"
        Clock.unschedule(self.hide_mantra)
        Clock.schedule_once(self.hide_mantra, 0.7)

        self.play_sound()
        self.flower_widget.trigger_flowers()

    def reset_counter(self, instance):
        reset_db_counts()
        self.current_count = 0
        self.count_label.text = "0"
        self.mala_label.text = "माला पूर्ण: 0  |  कुल जाप: 0"

if __name__ == '__main__':
    SambhSadashivApp().run()
