import os
import math
import urllib.request
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.graphics import Color, Ellipse, Line, Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation
from kivy.clock import Clock
from datetime import datetime

# Font setup for Devanagari (Hindi)
FONT_PATH = "NotoSansDevanagari.ttf"
if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
    try:
        urllib.request.urlretrieve(font_url, FONT_PATH)
    except Exception as e:
        print("Font download error:", e)

if os.path.exists(FONT_PATH):
    LabelBase.register(name="Hindi", fn_regular=FONT_PATH)

def to_devanagari(num):
    return str(num).translate(str.maketrans("0123456789", "०१२३४५६७८९"))

# --- CENTRAL GLOWING OM MANDALA (Interactive Tap Target) ---
class SacredOmMandala(FloatLayout):
    def __init__(self, on_tap_callback, **kwargs):
        super().__init__(**kwargs)
        self.on_tap_callback = on_tap_callback
        self.angle = 0
        self.bead_progress = 0  # 0 to 108

        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=0, axis=(0, 0, 1))
            
            # Outer Temple Ring (Gold)
            self.col_gold = Color(0.78, 0.57, 0.16, 0.4)
            self.ring_outer = Line(circle=(0, 0, 140), width=2)
            
            # Mala Beads Ring
            self.col_saffron = Color(1.0, 0.42, 0.21, 0.8)
            self.ring_inner = Line(circle=(0, 0, 110), width=3)
            
            # Glowing Aura Behind OM
            self.col_aura = Color(0.48, 0.18, 0.74, 0.25)
            self.aura = Ellipse(pos=(-100, -100), size=(200, 200))
            
            PopMatrix()

        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}
        self.om_label = Label(
            text="🕉️",
            font_size='90sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1.0, 0.82, 0.35, 1),
            **font_kw
        )
        self.add_widget(self.om_label)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, instance, value):
        cx, cy = self.center_x, self.center_y
        self.rot.origin = (cx, cy)
        self.ring_outer.circle = (cx, cy, self.width * 0.42)
        self.ring_inner.circle = (cx, cy, self.width * 0.35)
        
        aura_size = self.width * 0.55
        self.aura.pos = (cx - aura_size / 2, cy - aura_size / 2)
        self.aura.size = (aura_size, aura_size)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Pulse & Rotate Animation on Tap
            anim = Animation(angle=self.rot.angle + 30, d=0.25, t='out_quad')
            anim.start(self.rot)
            
            # Glow scale effect
            anim_label = Animation(font_size='105sp', d=0.1) + Animation(font_size='90sp', d=0.15)
            anim_label.start(self.om_label)
            
            self.on_tap_callback()
            return True
        return super().on_touch_down(touch)

# --- MAIN SACRED TEMPLE APP ---
class SambhSadashivApp(App):
    def build(self):
        self.mantra_counts = {
            "साम्ब सदाशिव": 0,
            "ॐ नमः शिवाय": 0,
            "हरे कृष्णा": 0,
            "श्री राम": 0,
            "गायत्री मंत्र": 0
        }
        self.current_mantra = "साम्ब सदाशिव"
        self.target_count = 108

        self.root = FloatLayout()

        # Background - Deep Temple Void (#0A0514)
        with self.root.canvas.before:
            Color(0.04, 0.02, 0.08, 1) # #0A0514
            self.bg_rect = Rectangle(pos=self.root.pos, size=self.root.size)
        self.root.bind(pos=self.update_bg, size=self.update_bg)

        main_box = BoxLayout(orientation='vertical', padding=[20, 24, 20, 20], spacing=12)
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}

        # 1. Header Bar (Temple Night Aesthetic)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        self.time_lbl = Label(text="", font_size='13sp', color=(0.78, 0.57, 0.26, 1), bold=True, **font_kw)
        header.add_widget(self.time_lbl)

        btn_settings = Button(text="⚙️", size_hint=(0.18, 1), font_size='18sp', background_color=(0.1, 0.04, 0.18, 0.9), color=(1,0.8,0.4,1))
        btn_settings.bind(on_press=self.open_settings)
        header.add_widget(btn_settings)
        main_box.add_widget(header)

        # 2. Mantra Selector Spinner
        spin_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        self.spinner = Spinner(
            text=self.current_mantra,
            values=list(self.mantra_counts.keys()),
            size_hint=(0.75, 1),
            background_color=(0.1, 0.04, 0.18, 0.95),
            color=(1, 0.85, 0.4, 1),
            font_size='16sp',
            **font_kw
        )
        self.spinner.bind(text=self.on_mantra_change)
        spin_box.add_widget(self.spinner)

        btn_add = Button(text="+", size_hint=(0.25, 1), background_color=(1.0, 0.42, 0.21, 0.9), font_size='22sp', bold=True)
        btn_add.bind(on_press=self.open_add_popup)
        spin_box.add_widget(btn_add)
        main_box.add_widget(spin_box)

        # 3. Main Counter Title
        self.mantra_title = Label(text=f"✨ {self.current_mantra} ✨", font_size='22sp', bold=True, color=(1.0, 0.82, 0.35, 1), size_hint=(1, 0.08), **font_kw)
        main_box.add_widget(self.mantra_title)

        # 4. Sacred OM Central Mandala Target
        self.mandala_container = FloatLayout(size_hint=(1, 0.45))
        self.mandala = SacredOmMandala(on_tap_callback=self.increment_counter, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.mandala_container.add_widget(self.mandala)
        main_box.add_widget(self.mandala_container)

        # 5. Live Digital Devanagari Counter & Mala Progress
        self.count_lbl = Label(text="०", font_size='55sp', bold=True, color=(1.0, 0.42, 0.21, 1), size_hint=(1, 0.12), **font_kw)
        main_box.add_widget(self.count_lbl)

        self.mala_lbl = Label(text="माला पूर्ण: ०  |  मनका: ०/१०८", font_size='15sp', color=(0.8, 0.7, 0.9, 1), size_hint=(1, 0.06), **font_kw)
        main_box.add_widget(self.mala_lbl)

        # 6. Bottom Action Controls
        bottom_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.09), spacing=12)
        
        btn_reset = Button(text="🔄 रीसेट", font_size='14sp', background_color=(0.5, 0.1, 0.1, 0.85), color=(1,1,1,1), **font_kw)
        btn_reset.bind(on_press=self.reset_counter)
        bottom_box.add_widget(btn_reset)

        main_box.add_widget(bottom_box)

        self.root.add_widget(main_box)
        Clock.schedule_interval(self.update_time, 1)
        return self.root

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def increment_counter(self):
        count = self.mantra_counts[self.current_mantra] + 1
        self.mantra_counts[self.current_mantra] = count
        self.update_display()

    def update_display(self):
        count = self.mantra_counts[self.current_mantra]
        beads = count % self.target_count
        completed = count // self.target_count

        self.count_lbl.text = to_devanagari(count)
        self.mala_lbl.text = f"माला पूर्ण: {to_devanagari(completed)}  |  मनका: {to_devanagari(beads)}/{to_devanagari(108)}"

    def reset_counter(self, instance):
        self.mantra_counts[self.current_mantra] = 0
        self.update_display()

    def on_mantra_change(self, spinner, text):
        self.current_mantra = text
        self.mantra_title.text = f"✨ {text} ✨"
        self.update_display()

    def open_add_popup(self, instance):
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}
        content = BoxLayout(orientation='vertical', padding=12, spacing=10)
        self.txt_input = TextInput(hint_text="नया मंत्र लिखें...", multiline=False, font_size='16sp', **font_kw)
        content.add_widget(self.txt_input)

        btn_save = Button(text="जोड़ें", size_hint=(1, 0.4), background_color=(1.0, 0.42, 0.21, 1), **font_kw)
        content.add_widget(btn_save)

        popup = Popup(title="नया मंत्र दर्ज करें", content=content, size_hint=(0.85, 0.3), **font_kw)
        
        def save(btn):
            val = self.txt_input.text.strip()
            if val and val not in self.mantra_counts:
                self.mantra_counts[val] = 0
                self.spinner.values = list(self.mantra_counts.keys())
                self.spinner.text = val
            popup.dismiss()

        btn_save.bind(on_press=save)
        popup.open()

    def open_settings(self, instance):
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(text="🛕 Sacred Temple Theme Active", font_size='16sp', bold=True, **font_kw))
        content.add_widget(Label(text="अद्वितीय अनुभव के लिए केंद्रीय ॐ प्रतीक पर टैप करें।", font_size='12sp', **font_kw))
        
        btn_close = Button(text="ठीक है", size_hint=(1, 0.35), background_color=(0.78, 0.57, 0.26, 1), **font_kw)
        popup = Popup(title="सेटिंग्स", content=content, size_hint=(0.8, 0.35), **font_kw)
        btn_close.bind(on_press=popup.dismiss)
        content.add_widget(btn_close)
        popup.open()

    def update_time(self, dt):
        now = datetime.now()
        self.time_lbl.text = now.strftime("📅 %d %b %Y  |  ⏰ %I:%M:%S %p")

if __name__ == '__main__':
    SambhSadashivApp().run()
