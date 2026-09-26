import os
import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from datetime import datetime

# 1. Automatic Hindi Font Setup
FONT_PATH = "NotoSansDevanagari.ttf"
if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
    try:
        urllib.request.urlretrieve(font_url, FONT_PATH)
    except Exception as e:
        print("Font download error:", e)

if os.path.exists(FONT_PATH):
    LabelBase.register(name="Hindi", fn_regular=FONT_PATH)

# Helper function to convert standard digits to Hindi Devanagari numerals
def to_devanagari(num):
    hindi_digits = str(num).translate(str.maketrans("0123456789", "०१२३४५६७८९"))
    return hindi_digits

# Custom Glassmorphic Card Container with Borders
class ModernGlassCard(BoxLayout):
    def __init__(self, bg_color=(0.08, 0.1, 0.15, 0.7), border_color=(1, 1, 1, 0.15), radius=[24,], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
            self.line_color = Color(*border_color)
            self.line = Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], radius[0]), width=1.2)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.line.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 24)

    def set_theme_colors(self, bg_col, border_col):
        self.rect_color.rgba = bg_col
        self.line_color.rgba = border_col

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
        self.counter_type = "Standard (1, 2, 3)"
        self.current_theme = "Glass Dark"

        # Wallpapers
        self.wallpapers = ['bg1.jpg', 'bg2.jpg', 'bg3.jpg']
        self.wp_index = 0

        # Root Layout
        self.root = FloatLayout()

        # Background Image
        self.bg_image = Image(
            source=self.wallpapers[0] if os.path.exists(self.wallpapers[0]) else '',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.root.add_widget(self.bg_image)

        # Main Layout Box
        main_box = BoxLayout(orientation='vertical', padding=[16, 20, 16, 16], spacing=10)
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}

        # --- TOP HEADER BAR ---
        self.header_card = ModernGlassCard(orientation='horizontal', size_hint=(1, 0.08), padding=[12, 6])
        self.time_lbl = Label(text="", font_size='13sp', color=(1, 0.85, 0.4, 1), bold=True, **font_kw)
        self.header_card.add_widget(self.time_lbl)

        btn_settings = Button(text="⚙️ सेटिंग्स", size_hint=(0.32, 1), font_size='13sp', background_color=(0.2, 0.3, 0.5, 0.9), **font_kw)
        btn_settings.bind(on_press=self.open_settings_popup)
        self.header_card.add_widget(btn_settings)
        main_box.add_widget(self.header_card)

        # --- MANTRA SELECTOR CARD ---
        self.select_card = ModernGlassCard(orientation='vertical', size_hint=(1, 0.14), padding=10, spacing=4)
        select_lbl = Label(text="मंत्र चयन (Select Mantra):", font_size='12sp', color=(0.85, 0.85, 0.9, 1), size_hint=(1, 0.3), **font_kw)
        self.select_card.add_widget(select_lbl)

        spin_box = BoxLayout(orientation='horizontal', spacing=8, size_hint=(1, 0.7))
        self.spinner = Spinner(
            text=self.current_mantra,
            values=list(self.mantra_counts.keys()),
            size_hint=(0.72, 1),
            background_color=(0.12, 0.18, 0.28, 0.9),
            color=(1, 1, 1, 1),
            font_size='16sp',
            **font_kw
        )
        self.spinner.bind(text=self.on_mantra_change)
        spin_box.add_widget(self.spinner)

        btn_add = Button(text="+ नया", size_hint=(0.28, 1), background_color=(0.15, 0.55, 0.35, 0.9), font_size='14sp', bold=True, **font_kw)
        btn_add.bind(on_press=self.open_add_popup)
        spin_box.add_widget(btn_add)
        self.select_card.add_widget(spin_box)
        main_box.add_widget(self.select_card)

        # --- MAIN COUNTER DISPLAY CARD ---
        self.counter_card = ModernGlassCard(orientation='vertical', size_hint=(1, 0.42), padding=12, spacing=6)
        
        self.mantra_title = Label(text=f"✨ {self.current_mantra} ✨", font_size='22sp', bold=True, color=(1, 0.8, 0.2, 1), size_hint=(1, 0.2), **font_kw)
        self.counter_card.add_widget(self.mantra_title)

        self.count_lbl = Label(text="0", font_size='70sp', bold=True, color=(0.2, 1, 0.75, 1), size_hint=(1, 0.48), **font_kw)
        self.counter_card.add_widget(self.count_lbl)

        # Mala Progress Bar
        self.progress_bar = ProgressBar(max=self.target_count, value=0, size_hint=(1, 0.08))
        self.counter_card.add_widget(self.progress_bar)

        self.mala_lbl = Label(text="माला पूर्ण: 0  |  मनका: 0/108", font_size='14sp', color=(0.9, 0.9, 0.95, 1), size_hint=(1, 0.24), **font_kw)
        self.counter_card.add_widget(self.mala_lbl)
        main_box.add_widget(self.counter_card)

        # --- GIANT TAP BUTTON ---
        self.btn_tap = Button(
            text="🙏 जाप करें (TAP)",
            size_hint=(1, 0.22),
            font_size='26sp',
            bold=True,
            background_normal='',
            background_color=(0.9, 0.4, 0.1, 0.92),
            **font_kw
        )
        self.btn_tap.bind(on_press=self.increment_counter)
        main_box.add_widget(self.btn_tap)

        # --- BOTTOM ACTION GRID ---
        bottom_grid = GridLayout(cols=2, spacing=8, size_hint=(1, 0.14))
        
        btn_wp = Button(text="🖼 वॉलपेपर बदलें", font_size='14sp', background_color=(0.2, 0.35, 0.55, 0.85), **font_kw)
        btn_wp.bind(on_press=self.change_wallpaper)
        bottom_grid.add_widget(btn_wp)

        btn_reset = Button(text="🔄 रीसेट", font_size='14sp', background_color=(0.75, 0.15, 0.15, 0.85), **font_kw)
        btn_reset.bind(on_press=self.reset_counter)
        bottom_grid.add_widget(btn_reset)

        main_box.add_widget(bottom_grid)

        self.root.add_widget(main_box)
        Clock.schedule_interval(self.update_time, 1)
        return self.root

    # --- SETTINGS POPUP MENU ---
    def open_settings_popup(self, instance):
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}
        content = BoxLayout(orientation='vertical', padding=15, spacing=12)

        # Theme Selector
        content.add_widget(Label(text="🎨 ऐप थीम चुनें (UI Theme):", font_size='14sp', bold=True, **font_kw))
        theme_spinner = Spinner(
            text=self.current_theme,
            values=["Glass Dark", "Saffron Gold", "Minimal Light"],
            size_hint=(1, 0.8),
            **font_kw
        )
        content.add_widget(theme_spinner)

        # Counter Type Selector
        content.add_widget(Label(text="🔢 डिफ़ॉल्ट काउंटर टाइप:", font_size='14sp', bold=True, **font_kw))
        counter_type_spinner = Spinner(
            text=self.counter_type,
            values=["Standard (1, 2, 3)", "Hindi (१, २, ३)", "Devotional Words (शिव/राम/ॐ)"],
            size_hint=(1, 0.8),
            **font_kw
        )
        content.add_widget(counter_type_spinner)

        # Gallery Custom Wallpaper Import
        btn_import_wp = Button(text="📁 गैलरी से वॉलपेपर चुनें", size_hint=(1, 0.9), background_color=(0.2, 0.5, 0.6, 1), **font_kw)
        btn_import_wp.bind(on_press=self.open_file_chooser)
        content.add_widget(btn_import_wp)

        # Close/Save Button
        btn_close = Button(text="लागू करें (Apply Settings)", size_hint=(1, 0.9), background_color=(0.1, 0.6, 0.3, 1), **font_kw)
        popup = Popup(title="⚙️ ऐप सेटिंग्स", content=content, size_hint=(0.9, 0.6), **font_kw)

        def apply_settings(btn):
            self.current_theme = theme_spinner.text
            self.counter_type = counter_type_spinner.text
            self.apply_theme(self.current_theme)
            self.update_display()
            popup.dismiss()

        btn_close.bind(on_press=apply_settings)
        content.add_widget(btn_close)
        popup.open()

    # --- Apply Dynamic Themes ---
    def apply_theme(self, theme_name):
        if theme_name == "Saffron Gold":
            bg_c = (0.25, 0.1, 0.02, 0.8)
            border_c = (1, 0.7, 0.2, 0.5)
            self.count_lbl.color = (1, 0.8, 0.1, 1)
        elif theme_name == "Minimal Light":
            bg_c = (0.95, 0.95, 0.98, 0.85)
            border_c = (0, 0, 0, 0.1)
            self.count_lbl.color = (0.05, 0.45, 0.85, 1)
        else:  # Glass Dark
            bg_c = (0.08, 0.1, 0.15, 0.7)
            border_c = (1, 1, 1, 0.15)
            self.count_lbl.color = (0.2, 1, 0.75, 1)

        self.header_card.set_theme_colors(bg_c, border_c)
        self.select_card.set_theme_colors(bg_c, border_c)
        self.counter_card.set_theme_colors(bg_c, border_c)

    # --- File Chooser for Importing Wallpapers ---
    def open_file_chooser(self, instance):
        font_kw = {'font_name': 'Hindi'} if os.path.exists(FONT_PATH) else {}
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView(filters=['*.jpg', '*.png', '*.jpeg'])
        content.add_widget(file_chooser)

        btn_select = Button(text="सेट करें", size_hint=(1, 0.15), background_color=(0.1, 0.6, 0.3, 1), **font_kw)
        popup = Popup(title="इमेज फाइल चुनें", content=content, size_hint=(0.95, 0.85), **font_kw)

        def set_image(btn):
            if file_chooser.selection:
                selected_file = file_chooser.selection[0]
                self.bg_image.source = selected_file
                self.bg_image.reload()
            popup.dismiss()

        btn_select.bind(on_press=set_image)
        content.add_widget(btn_select)
        popup.open()

    # --- Core Logic Functions ---
    def increment_counter(self, instance):
        count = self.mantra_counts[self.current_mantra] + 1
        self.mantra_counts[self.current_mantra] = count
        self.update_display()

    def update_display(self):
        count = self.mantra_counts[self.current_mantra]
        beads = count % self.target_count
        completed = count // self.target_count

        # Display based on counter type selected
        if self.counter_type == "Hindi (१, २, ३)":
            self.count_lbl.text = to_devanagari(count)
            self.mala_lbl.text = f"माला पूर्ण: {to_devanagari(completed)}  |  मनका: {to_devanagari(beads)}/{to_devanagari(self.target_count)}"
        elif self.counter_type == "Devotional Words (शिव/राम/ॐ)":
            words = ["ॐ", "शिव", "हर हर महादेव", "सदाशिव", "जय श्री राम"]
            self.count_lbl.text = words[count % len(words)]
            self.mala_lbl.text = f"कुल जाप संख्या: {count}  |  माला: {completed}"
        else:
            self.count_lbl.text = str(count)
            self.mala_lbl.text = f"माला पूर्ण: {completed}  |  मनका: {beads}/{self.target_count}"

        self.progress_bar.max = self.target_count
        self.progress_bar.value = beads if beads != 0 else (self.target_count if count > 0 else 0)

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
        self.txt_input = TextInput(hint_text="मंत्र का नाम दर्ज करें...", multiline=False, font_size='16sp', **font_kw)
        content.add_widget(self.txt_input)

        btn_save = Button(text="जोड़ें (Save)", size_hint=(1, 0.4), background_color=(0.1, 0.6, 0.3, 1), **font_kw)
        content.add_widget(btn_save)

        popup = Popup(title="नया मंत्र जोड़ें", content=content, size_hint=(0.85, 0.32), **font_kw)
        
        def save_mantra(btn_inst):
            val = self.txt_input.text.strip()
            if val and val not in self.mantra_counts:
                self.mantra_counts[val] = 0
                self.spinner.values = list(self.mantra_counts.keys())
                self.spinner.text = val
            popup.dismiss()

        btn_save.bind(on_press=save_mantra)
        popup.open()

    def change_wallpaper(self, instance):
        if self.wallpapers:
            self.wp_index = (self.wp_index + 1) % len(self.wallpapers)
            wp = self.wallpapers[self.wp_index]
            if os.path.exists(wp):
                self.bg_image.source = wp
                self.bg_image.reload()

    def update_time(self, dt):
        now = datetime.now()
        self.time_lbl.text = now.strftime("📅 %d %b %Y  |  ⏰ %I:%M:%S %p")

if __name__ == '__main__':
    SambhSadashivApp().run()
