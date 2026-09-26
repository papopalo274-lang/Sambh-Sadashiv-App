import os
import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.clock import Clock
from datetime import datetime

# 1. Hindi Font Download & Register Setup
FONT_PATH = "NotoSansDevanagari.ttf"
if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
    try:
        urllib.request.urlretrieve(font_url, FONT_PATH)
    except Exception as e:
        print("Font download error:", e)

if os.path.exists(FONT_PATH):
    LabelBase.register(name="Hindi", fn_regular=FONT_PATH)

class SambhSadashivApp(App):
    def build(self):
        self.counter = 0
        self.wallpapers = ['bg1.jpg', 'bg2.jpg']  # Default wallpapers list
        self.current_wp_index = 0

        # Root Layout (FloatLayout to layer background image below controls)
        self.root_layout = FloatLayout()

        # Background Image Widget
        self.bg_image = Image(
            source=self.wallpapers[self.current_wp_index] if os.path.exists(self.wallpapers[0]) else '',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.root_layout.add_widget(self.bg_image)

        # UI Container (Vertical BoxLayout)
        ui_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Time/Date Label
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}
        self.time_label = Label(text="", size_hint=(1, 0.1), font_size='18sp', **font_kw)
        ui_layout.add_widget(self.time_label)

        # Title Label
        title_label = Label(text="— साम्ब सदाशिव —", size_hint=(1, 0.1), font_size='24sp', bold=True, **font_kw)
        ui_layout.add_widget(title_label)

        # Counter Label
        self.counter_label = Label(text="0", size_hint=(1, 0.3), font_size='60sp', bold=True, color=(0, 1, 0.8, 1))
        ui_layout.add_widget(self.counter_label)

        # Increment Button (जाप बटन)
        btn_count = Button(text="साम्ब सदाशिव (जाप)", size_hint=(1, 0.2), font_size='22sp', background_color=(0.1, 0.4, 0.6, 1), **font_kw)
        btn_count.bind(on_press=self.increment_counter)
        ui_layout.add_widget(btn_count)

        # Controls Row (Wallpaper Change & Reset)
        controls = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        
        btn_wp = Button(text="वॉलपेपर बदलें", font_size='16sp', **font_kw)
        btn_wp.bind(on_press=self.change_wallpaper)
        controls.add_widget(btn_wp)

        btn_reset = Button(text="रीसेट (Reset)", font_size='16sp', background_color=(0.6, 0.1, 0.1, 1), **font_kw)
        btn_reset.bind(on_press=self.reset_counter)
        controls.add_widget(btn_reset)

        ui_layout.add_widget(controls)
        self.root_layout.add_widget(ui_layout)

        # Clock updates for live time
        Clock.schedule_interval(self.update_time, 1)
        return self.root_layout

    def increment_counter(self, instance):
        self.counter += 1
        self.counter_label.text = str(self.counter)

    def reset_counter(self, instance):
        self.counter = 0
        self.counter_label.text = str(self.counter)

    def change_wallpaper(self, instance):
        # Wallpaper Transition logic
        if self.wallpapers:
            self.current_wp_index = (self.current_wp_index + 1) % len(self.wallpapers)
            wp_path = self.wallpapers[self.current_wp_index]
            if os.path.exists(wp_path):
                self.bg_image.source = wp_path
                self.bg_image.reload()

    def update_time(self, dt):
        now = datetime.now()
        self.time_label.text = now.strftime("%I:%M:%S %p | %d %b %Y")

if __name__ == '__main__':
    SambhSadashivApp().run()
